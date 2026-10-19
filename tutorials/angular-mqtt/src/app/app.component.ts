import { Component, inject } from "@angular/core";
import { MqttService } from "./mqtt.service";
import { SensorPanelComponent } from "./sensor-panel.component";

@Component({
  selector: "app-root",
  standalone: true,
  imports: [SensorPanelComponent],
  template: `<h1>Angular MQTT Demo</h1><app-sensor-panel />`,
})
export class AppComponent {
  constructor() {
    inject(MqttService).connect("wss://broker.connectmq.com:8084/mqtt");
  }
}
