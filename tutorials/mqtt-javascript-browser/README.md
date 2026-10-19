# MQTT in the Browser with JavaScript: A Minimal Client in One HTML Page

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-javascript-browser-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-javascript-browser-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Build a single HTML page that connects to broker.connectmq.com over secure WebSocket, subscribes, publishes and shows live messages using MQTT.js, with no build step and no backend.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-javascript-browser-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-javascript-browser-intro)

📖 **Full step-by-step tutorial:** [MQTT in the Browser with JavaScript: A Minimal Client in One HTML Page](https://connectmq.com/blog/mqtt-javascript-browser/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-javascript-browser-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-javascript-browser-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`mqtt-client.html`](mqtt-client.html) | Single-page MQTT.js browser client: connects over secure WebSocket, subscribes, publishes and logs live messages |

## Requirements

- Any modern web browser (no build step, no backend)
- MQTT.js 5 (loaded from the unpkg CDN by the page)
- Optional: `mosquitto_sub` / `mosquitto_pub` to test from a terminal

## Run it on the free public broker

1. Open `mqtt-client.html` in any modern browser. It uses `wss://broker.connectmq.com:8084/mqtt` and generates a random topic prefix.
2. Click **Connect**, then **Subscribe**, then **Publish**. The message comes back to the same page because you are subscribed to `prefix/#`.
3. Watch the messages from a terminal (replace the prefix with the one your page shows):

   ```bash
   mosquitto_sub -h broker.connectmq.com -p 1883 -i cli-watch-7f3a -t 'connectmq/demo/YOUR_PREFIX/#' -v
   ```

4. Publish from the terminal and the browser log updates instantly:

   ```bash
   mosquitto_pub -h broker.connectmq.com -p 1883 -i cli-pub-7f3a -t 'connectmq/demo/YOUR_PREFIX/sensors/room1' -m '{"temperature": 23.1}'
   ```

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-javascript-browser-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-javascript-browser-private) — the **Serverless (Free)** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. In `mqtt-client.html`, change the URL field to your broker's secure WebSocket endpoint (`wss://YOUR_BROKER_HOST:8084/mqtt`) and add the credentials to the `mqtt.connect()` options, as the comment in the page shows:

   ```js
   // For a private ConnectMQ broker add:
   // username: "YOUR_USERNAME",
   // password: "YOUR_PASSWORD"
   ```

   Anything in browser JavaScript is readable in DevTools: use separate, low-privilege credentials for browser dashboards, or ask the user to type them at runtime.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [MQTT in the Browser with JavaScript: A Minimal Client in One HTML Page](https://connectmq.com/blog/mqtt-javascript-browser/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-javascript-browser-related) — the full tutorial with explanations
- 🧩 [Node.js basic example](../../nodejs/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-javascript-browser-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-javascript-browser-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-javascript-browser-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-javascript-browser-footer">Blog</a>
</p>
