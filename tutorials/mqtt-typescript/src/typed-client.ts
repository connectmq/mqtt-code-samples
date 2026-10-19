import mqtt, { IClientOptions, MqttClient } from "mqtt";
import { contracts, ContractKey, PayloadOf, TopicArgs } from "./contracts.js";

type Handler<K extends ContractKey> = (payload: PayloadOf<K>, topic: string) => void;

export function topicMatches(filter: string, topic: string): boolean {
  const f = filter.split("/");
  const t = topic.split("/");
  for (let i = 0; i < f.length; i++) {
    if (f[i] === "#") return true;
    if (i >= t.length) return false;
    if (f[i] !== "+" && f[i] !== t[i]) return false;
  }
  return f.length === t.length;
}

export class TypedMqttClient {
  private readonly client: MqttClient;
  private readonly handlers = new Map<ContractKey, Set<Handler<any>>>();

  constructor(
    url: string,
    options: IClientOptions,
    private readonly onInvalid: (topic: string, error: unknown) => void = (topic, error) =>
      console.warn(`Invalid payload on ${topic}:`, error)
  ) {
    this.client = mqtt.connect(url, { protocolVersion: 5, reconnectPeriod: 2000, ...options });

    this.client.on("connect", () => {
      for (const key of this.handlers.keys()) {
        const c = contracts[key];
        this.client.subscribe(c.filter, { qos: c.qos });
      }
    });

    this.client.on("message", (topic, buffer) => this.dispatch(topic, buffer));
    this.client.on("error", (err) => console.error("MQTT error:", err.message));
  }

  async publish<K extends ContractKey>(key: K, args: TopicArgs<K>, payload: PayloadOf<K>): Promise<void> {
    const c = contracts[key];
    const validated = c.schema.parse(payload); // never send what we would reject ourselves
    const topic = (c.topic as (...a: unknown[]) => string)(...args);
    await this.client.publishAsync(topic, JSON.stringify(validated), { qos: c.qos, retain: c.retain });
  }

  subscribe<K extends ContractKey>(key: K, handler: Handler<K>): () => void {
    let set = this.handlers.get(key);
    if (!set) {
      set = new Set();
      this.handlers.set(key, set);
      if (this.client.connected) {
        this.client.subscribe(contracts[key].filter, { qos: contracts[key].qos });
      }
    }
    set.add(handler);
    return () => {
      set!.delete(handler);
      if (set!.size === 0) {
        this.handlers.delete(key);
        this.client.unsubscribe(contracts[key].filter);
      }
    };
  }

  async close(): Promise<void> {
    await this.client.endAsync();
  }

  private dispatch(topic: string, buffer: Buffer): void {
    for (const [key, set] of this.handlers) {
      const c = contracts[key];
      if (!topicMatches(c.filter, topic)) continue;
      let raw: unknown;
      try {
        raw = JSON.parse(buffer.toString());
      } catch (err) {
        this.onInvalid(topic, err);
        continue;
      }
      const result = c.schema.safeParse(raw);
      if (!result.success) {
        this.onInvalid(topic, result.error.issues);
        continue;
      }
      for (const handler of set) handler(result.data, topic);
    }
  }
}
