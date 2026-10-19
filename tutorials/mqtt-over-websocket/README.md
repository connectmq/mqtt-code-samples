# MQTT over WebSocket: Connect a Browser to an MQTT Broker with MQTT.js

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-over-websocket-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-over-websocket-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Browsers cannot open raw TCP sockets, so web apps speak MQTT over WebSocket. Build a working browser client and a Node.js client against broker.connectmq.com and learn how to fix the most common connection errors.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-over-websocket-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-over-websocket-intro)

📖 **Full step-by-step tutorial:** [MQTT over WebSocket: Connect a Browser to an MQTT Broker with MQTT.js](https://connectmq.com/blog/mqtt-over-websocket/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-over-websocket-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-over-websocket-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`index.html`](index.html) | Self-contained browser page: MQTT.js over `wss://broker.connectmq.com:8084/mqtt`, subscribes to a unique topic and publishes from an input box |
| [`ws-client.mjs`](ws-client.mjs) | Node.js client over secure WebSocket: subscribes, publishes one JSON message, prints it and exits |
| [`package.json`](package.json) | Node.js project with the `mqtt` dependency |

## Requirements

- A modern web browser for `index.html` (MQTT.js 5 is loaded from the unpkg CDN)
- Node.js with MQTT.js (`mqtt` package) for `ws-client.mjs`
- Optional: `mosquitto_sub` to watch the browser's messages from a terminal

## Run it on the free public broker

1. Open `index.html` in a browser. It connects to `wss://broker.connectmq.com:8084/mqtt`, subscribes to `connectmq/demo/<id>/chat` and echoes what you publish.
2. Watch the browser's messages from a terminal (replace `abc12345` with the id shown in the page's topic):

   ```bash
   mosquitto_sub -h broker.connectmq.com -p 1883 -i cli-watch-abc12345 -t "connectmq/demo/abc12345/#" -v
   ```

3. Run the Node.js client:

   ```bash
   npm install mqtt
   node ws-client.mjs
   ```

   The output looks similar to this:

   ```text
   Connected, CONNACK properties: { receiveMaximum: 16, topicAliasMaximum: 65535 }
   Granted: [ { topic: 'connectmq/demo/4df8521c/hello', qos: 1, nl: false, rap: false, rh: 0 } ]
   Received on connectmq/demo/4df8521c/hello: {"temp":21.5,"ts":1790000000000}
   ```

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-over-websocket-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-over-websocket-private) — the **Serverless (Free)** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. Replace the `mqtt.connect(...)` call in `index.html` (or `ws-client.mjs`) with your broker's secure WebSocket URL and the generated credentials:

   ```javascript
   const client = mqtt.connect("wss://broker.connectmq.com:8084/mqtt", {
     clientId: "YOUR_CLIENT_ID_dashboard",
     username: "YOUR_USERNAME",
     password: "YOUR_PASSWORD",
     protocolVersion: 5,
     keepalive: 30,
   });
   ```

   Use your broker's host in the URL, always use `wss://` (port 8084, path `/mqtt`) so credentials are encrypted, and give the web app its own credentials rather than reusing device credentials. On a private broker, client IDs are restricted to the issued client ID and its `_suffix` variants (`YOUR_CLIENT_ID_tab1`, `YOUR_CLIENT_ID_tab2`, ...).

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [MQTT over WebSocket: Connect a Browser to an MQTT Broker with MQTT.js](https://connectmq.com/blog/mqtt-over-websocket/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-over-websocket-related) — the full tutorial with explanations
- 🧩 [Node.js basic example](../../nodejs/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-over-websocket-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-over-websocket-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-over-websocket-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-over-websocket-footer">Blog</a>
</p>
