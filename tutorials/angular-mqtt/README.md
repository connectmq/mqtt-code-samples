# Angular MQTT Tutorial with RxJS, MQTT.js and ngx-mqtt

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-angular-mqtt-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-angular-mqtt-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Wire an Angular service to an MQTT broker over secure WebSocket, expose topics as RxJS observables with wildcard matching, render them with the async pipe, and compare the approach with ngx-mqtt.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-angular-mqtt-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-angular-mqtt-intro)

📖 **Full step-by-step tutorial:** [Angular MQTT Tutorial with RxJS, MQTT.js and ngx-mqtt](https://connectmq.com/blog/angular-mqtt/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-angular-mqtt-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-angular-mqtt-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`src/app/mqtt.service.ts`](src/app/mqtt.service.ts) | Root-level `MqttService`: one MQTT.js connection over `wss://`, topic filters as ref-counted RxJS observables, `publish()`. |
| [`src/app/sensor-panel.component.ts`](src/app/sensor-panel.component.ts) | Standalone component that renders the latest telemetry per device with the `async` pipe and publishes a toggle command. |
| [`src/app/app.component.ts`](src/app/app.component.ts) | Root component that connects the service once at startup. |

## Requirements

- Node.js and the Angular CLI (a current Angular version with standalone components and `inject()`)
- MQTT.js (`mqtt` package, v5 recommended)
- Optional: `mosquitto_pub` to publish test data

## Run it on the free public broker

1. Create the project and install MQTT.js:

   ```bash
   npm install -g @angular/cli
   ng new angular-mqtt-demo --standalone --style=css --routing=false
   cd angular-mqtt-demo
   npm install mqtt
   ```

2. Copy the three files from `src/app/` into the new project (replacing the generated `app.component.ts`). Change `PREFIX` in `sensor-panel.component.ts` to your own random prefix.
3. Start the dev server with `ng serve`, then publish test data:

   ```bash
   mosquitto_pub -h broker.connectmq.com -p 1883 -i ng-pub-6b19 \
     -t connectmq/demo/ng-6b19/pump1/telemetry -m '{"temperature": 36.5, "humidity": 48}'
   ```

   The card for `pump1` appears immediately.

Prefer ngx-mqtt? The post shows the equivalent bootstrap configuration for `main.ts`:

```typescript
import { importProvidersFrom } from "@angular/core";
import { bootstrapApplication } from "@angular/platform-browser";
import { IMqttServiceOptions, MqttModule } from "ngx-mqtt";
import { AppComponent } from "./app/app.component";

const MQTT_OPTIONS: IMqttServiceOptions = {
  hostname: "broker.connectmq.com",
  port: 8084,
  path: "/mqtt",
  protocol: "wss",
  clientId: `ngx-${Math.random().toString(16).slice(2, 10)}`,
};

bootstrapApplication(AppComponent, {
  providers: [importProvidersFrom(MqttModule.forRoot(MQTT_OPTIONS))],
});
```

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-angular-mqtt-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-angular-mqtt-private) — the **Free** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. In `src/app/app.component.ts`, pass your broker host and credentials to `connect()` (browsers always use secure WebSocket on port 8084 with the `/mqtt` path):

   ```typescript
   connect("wss://YOUR_BROKER_HOST:8084/mqtt", { username, password, clientId })
   ```

   Frontend code is visible to users, so use a dedicated dashboard credential (or one issued by your backend) and route sensitive commands through your backend.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [Angular MQTT Tutorial with RxJS, MQTT.js and ngx-mqtt](https://connectmq.com/blog/angular-mqtt/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-angular-mqtt-related) — the full tutorial with explanations
- 🧩 [Node.js basic example](../../nodejs/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-angular-mqtt-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-angular-mqtt-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-angular-mqtt-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-angular-mqtt-footer">Blog</a>
</p>
