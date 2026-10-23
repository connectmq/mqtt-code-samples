# Next.js MQTT: Server and Client Integration Patterns That Actually Work

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-next-js-mqtt-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-next-js-mqtt-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Learn the three ways to use MQTT in a Next.js App Router project: client components over secure WebSocket, server route handlers that publish with private credentials, and a Server-Sent Events bridge.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-next-js-mqtt-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-next-js-mqtt-intro)

📖 **Full step-by-step tutorial:** [Next.js MQTT: Server and Client Integration Patterns That Actually Work](https://connectmq.com/blog/next-js-mqtt/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-next-js-mqtt-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-next-js-mqtt-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`app/hooks/useMqtt.js`](app/hooks/useMqtt.js) | Pattern 1: client-side React hook that connects over `wss://` 8084, subscribes and keeps the last 100 messages |
| [`app/live/page.jsx`](app/live/page.jsx) | Client page that lists live messages from `connectmq/demo/next-k7f3q2/sensors/#` |
| [`lib/mqtt-server.js`](lib/mqtt-server.js) | Server-side MQTT client singleton cached on `globalThis`, configured from environment variables |
| [`app/api/command/route.js`](app/api/command/route.js) | Pattern 2: `POST` route handler that validates `deviceId` and `action` and publishes a command with QoS 1 |
| [`app/api/notice/route.js`](app/api/notice/route.js) | Serverless variant: connect, publish and close in the same request |
| [`app/api/stream/route.js`](app/api/stream/route.js) | Pattern 3: Server-Sent Events route that fans MQTT messages out to browsers |
| [`package.json`](package.json) | The `mqtt` dependency the post installs |

## Requirements

- A Next.js project using the App Router, running on the Node.js runtime (not Edge)
- [MQTT.js](https://github.com/mqttjs/MQTT.js) v5 (`npm install mqtt`)
- The `@/` import alias (default in `create-next-app` projects) for the route handlers
- Optional: `mosquitto_pub` to send test readings

## Run it on the free public broker

1. Copy the `app/` and `lib/` folders into your Next.js App Router project and install MQTT.js:

   ```bash
   npm install mqtt
   ```

2. Start the dev server (`npm run dev`), open `/live`, and publish a test reading from a terminal:

   ```bash
   mosquitto_pub -h broker.connectmq.com -p 1883 -i next-test-3b1c -t 'connectmq/demo/next-k7f3q2/sensors/room1' -m '{"t":22.4}'
   ```

   Change `next-k7f3q2` to your own random prefix in every file.

3. Send a command through the route handler (`POST /api/command` with JSON `{"deviceId": "...", "action": "on"}`) and watch it arrive on `connectmq/demo/next-k7f3q2/devices/<deviceId>/cmd`.

4. For the SSE bridge (Pattern 3), the post says to subscribe once in the singleton. Add this inside `getMqttClient` in `lib/mqtt-server.js`, after creating the client:

   ```javascript
   globalForMqtt.__mqttClient.on("connect", () => {
     globalForMqtt.__mqttClient.subscribe("connectmq/demo/next-k7f3q2/sensors/#", { qos: 1 });
   });
   ```

   Then use `new EventSource("/api/stream")` in a client component. SSE only works on a long-running Node.js server, not on serverless functions with short timeouts.

The browser URL can be overridden with `NEXT_PUBLIC_MQTT_URL` (default `wss://broker.connectmq.com:8084/mqtt`). Anything prefixed with `NEXT_PUBLIC_` ends up in the client bundle, so never put a password there.

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-next-js-mqtt-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-next-js-mqtt-private) — the **Free** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. The server code (`lib/mqtt-server.js`, `app/api/notice/route.js`) reads its connection from environment variables. Put them in `.env.local`:

   ```bash
   MQTT_URL=mqtts://YOUR_BROKER_HOST:8883
   MQTT_USERNAME=YOUR_USERNAME
   MQTT_PASSWORD=YOUR_PASSWORD
   MQTT_CLIENT_ID=YOUR_CLIENT_ID
   ```

   For browser subscriptions in `app/hooks/useMqtt.js`, set `NEXT_PUBLIC_MQTT_URL=wss://YOUR_BROKER_HOST:8084/mqtt` and use only read-only credentials in the browser; route every command through `app/api/command/route.js`.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [Next.js MQTT: Server and Client Integration Patterns That Actually Work](https://connectmq.com/blog/next-js-mqtt/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-next-js-mqtt-related) — the full tutorial with explanations
- 🧩 [Node.js basic example](../../nodejs/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-next-js-mqtt-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-next-js-mqtt-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-next-js-mqtt-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-next-js-mqtt-footer">Blog</a>
</p>
