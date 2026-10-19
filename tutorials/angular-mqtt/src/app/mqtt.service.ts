import { Injectable, OnDestroy } from "@angular/core";
import { BehaviorSubject, Observable, Subject, filter, finalize, map, share } from "rxjs";
import mqtt, { IClientOptions, MqttClient } from "mqtt";

export interface MqttMessage<T = unknown> {
  topic: string;
  payload: T;
  retain: boolean;
  receivedAt: number;
}

export type ConnectionState = "connecting" | "connected" | "reconnecting" | "offline" | "closed";

/** MQTT topic filter matching with + and # wildcards. */
export function topicMatches(filterStr: string, topic: string): boolean {
  const f = filterStr.split("/");
  const t = topic.split("/");
  for (let i = 0; i < f.length; i++) {
    if (f[i] === "#") return true;
    if (i >= t.length) return false;
    if (f[i] !== "+" && f[i] !== t[i]) return false;
  }
  return f.length === t.length;
}

@Injectable({ providedIn: "root" })
export class MqttService implements OnDestroy {
  private client?: MqttClient;
  private readonly messages$ = new Subject<MqttMessage>();
  private readonly refCounts = new Map<string, number>();
  private readonly streams = new Map<string, Observable<MqttMessage>>();

  readonly state$ = new BehaviorSubject<ConnectionState>("closed");

  connect(url: string, options: IClientOptions = {}): void {
    if (this.client) return;
    this.state$.next("connecting");
    this.client = mqtt.connect(url, {
      protocolVersion: 5,
      reconnectPeriod: 3000,
      connectTimeout: 10000,
      clientId: `ng-${Math.random().toString(16).slice(2, 10)}`,
      ...options,
    });

    this.client.on("connect", () => {
      this.state$.next("connected");
      // restore all active subscriptions after (re)connect
      const filters = [...this.refCounts.keys()];
      if (filters.length) this.client!.subscribe(filters, { qos: 0 });
    });
    this.client.on("reconnect", () => this.state$.next("reconnecting"));
    this.client.on("offline", () => this.state$.next("offline"));
    this.client.on("error", (err) => console.error("MQTT error", err.message));
    this.client.on("message", (topic, payload, packet) => {
      const text = payload.toString();
      let parsed: unknown = text;
      try {
        parsed = JSON.parse(text);
      } catch {
        /* keep text */
      }
      this.messages$.next({ topic, payload: parsed, retain: packet.retain, receivedAt: Date.now() });
    });
  }

  observe<T = unknown>(topicFilter: string): Observable<MqttMessage<T>> {
    let stream = this.streams.get(topicFilter);
    if (!stream) {
      stream = new Observable<MqttMessage>((subscriber) => {
        this.addRef(topicFilter);
        const sub = this.messages$
          .pipe(filter((m) => topicMatches(topicFilter, m.topic)))
          .subscribe(subscriber);
        return () => sub.unsubscribe();
      }).pipe(
        finalize(() => this.removeRef(topicFilter)),
        share()
      );
      this.streams.set(topicFilter, stream);
    }
    return stream as Observable<MqttMessage<T>>;
  }

  observePayload<T = unknown>(topicFilter: string): Observable<T> {
    return this.observe<T>(topicFilter).pipe(map((m) => m.payload));
  }

  publish(topic: string, message: unknown, qos: 0 | 1 | 2 = 0, retain = false): Promise<void> {
    if (!this.client?.connected) return Promise.reject(new Error("MQTT not connected"));
    const body = typeof message === "string" ? message : JSON.stringify(message);
    return this.client.publishAsync(topic, body, { qos, retain }).then(() => undefined);
  }

  private addRef(topicFilter: string): void {
    const count = this.refCounts.get(topicFilter) ?? 0;
    this.refCounts.set(topicFilter, count + 1);
    if (count === 0 && this.client?.connected) this.client.subscribe(topicFilter, { qos: 0 });
  }

  private removeRef(topicFilter: string): void {
    const count = (this.refCounts.get(topicFilter) ?? 1) - 1;
    if (count > 0) {
      this.refCounts.set(topicFilter, count);
      return;
    }
    this.refCounts.delete(topicFilter);
    this.streams.delete(topicFilter);
    if (this.client?.connected) this.client.unsubscribe(topicFilter);
  }

  ngOnDestroy(): void {
    this.client?.end(true);
    this.state$.next("closed");
  }
}
