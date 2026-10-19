import { Component, inject } from "@angular/core";
import { AsyncPipe, DatePipe, JsonPipe } from "@angular/common";
import { map, scan } from "rxjs";
import { MqttService, MqttMessage } from "./mqtt.service";

interface Telemetry {
  temperature?: number;
  humidity?: number;
}

const PREFIX = "connectmq/demo/ng-6b19";

@Component({
  selector: "app-sensor-panel",
  standalone: true,
  imports: [AsyncPipe, DatePipe, JsonPipe],
  template: `
    <p>Connection: <strong>{{ mqtt.state$ | async }}</strong></p>
    @if (devices$ | async; as devices) {
      @for (d of devices; track d.topic) {
        <div class="card">
          <h3>{{ d.topic.split('/').at(-2) }}</h3>
          <p>{{ d.payload.temperature ?? '--' }} &deg;C, {{ d.payload.humidity ?? '--' }} %</p>
          <small>{{ d.receivedAt | date: 'mediumTime' }}</small>
        </div>
      }
    }
    <button (click)="toggle()" [disabled]="(mqtt.state$ | async) !== 'connected'">Toggle pump1</button>
  `,
})
export class SensorPanelComponent {
  readonly mqtt = inject(MqttService);

  readonly devices$ = this.mqtt.observe<Telemetry>(`${PREFIX}/+/telemetry`).pipe(
    scan((acc, msg) => {
      const next = new Map(acc);
      next.set(msg.topic, msg);
      return next;
    }, new Map<string, MqttMessage<Telemetry>>()),
    map((byTopic) => [...byTopic.values()])
  );

  toggle(): void {
    this.mqtt.publish(`${PREFIX}/pump1/cmd`, { action: "toggle" }, 1).catch(console.error);
  }
}
