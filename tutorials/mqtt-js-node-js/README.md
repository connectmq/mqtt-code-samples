# MQTT.js Node.js Tutorial: Publish, Subscribe, QoS and TLS

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-js-node-js-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-js-node-js-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Build a Node.js publisher and subscriber with MQTT.js v5, use the async API, QoS and Last Will, encrypt with TLS on port 8883, and tune reconnect options so your service survives network drops.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-js-node-js-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-js-node-js-intro)

📖 **Full step-by-step tutorial:** [MQTT.js Node.js Tutorial: Publish, Subscribe, QoS and TLS](https://connectmq.com/blog/mqtt-js-node-js/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-js-node-js-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-js-node-js-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`subscriber.js`](subscriber.js) | MQTT.js v5 subscriber over TLS (8883) that re-subscribes on every connect and parses JSON telemetry |
| [`publisher.js`](publisher.js) | Publishes 20 JSON readings with QoS 1, MQTT 5 properties and a retained Last Will status |
| [`private-broker.js`](private-broker.js) | Connects to a private broker with credentials from environment variables and a persistent session |
| [`package.json`](package.json) | ES module project with the `mqtt` dependency |

## Requirements

- Node.js 18 or newer (`node --version`)
- npm, pnpm or yarn
- MQTT.js v5 (`mqtt` package)
- Optional: `mosquitto_sub` to watch traffic from a second terminal

## Run it on the free public broker

1. Install the library (the post creates the project with `npm init -y` and `npm pkg set type=module`; `package.json` here already has `"type": "module"`):

   ```bash
   npm install mqtt
   ```

2. Change the `node-a71c` part of `PREFIX` in both scripts to your own random string.
3. Run both:

   ```bash
   node subscriber.js
   # in a second terminal
   node publisher.js
   ```

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-js-node-js-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-js-node-js-private) — the **Serverless (Free)** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. Use `private-broker.js`, which loads the broker host and credentials from environment variables and connects with TLS on port 8883:

   ```javascript
   const client = mqtt.connect(`mqtts://${process.env.MQTT_HOST}:8883`, {
     clientId: process.env.MQTT_CLIENT_ID,   // YOUR_CLIENT_ID from the portal
     username: process.env.MQTT_USERNAME,    // YOUR_USERNAME
     password: process.env.MQTT_PASSWORD,    // YOUR_PASSWORD
     protocolVersion: 5,
     clean: false,
     properties: { sessionExpiryInterval: 3600 },
   });
   ```

   Set `MQTT_HOST`, `MQTT_CLIENT_ID`, `MQTT_USERNAME` and `MQTT_PASSWORD`, then run `node private-broker.js`. To move `subscriber.js` and `publisher.js` as well, replace `broker.connectmq.com` with your host and add the same `username` and `password` options. ConnectMQ uses a Let's Encrypt certificate that Node.js trusts out of the box; never set `rejectUnauthorized: false`.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [MQTT.js Node.js Tutorial: Publish, Subscribe, QoS and TLS](https://connectmq.com/blog/mqtt-js-node-js/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-js-node-js-related) — the full tutorial with explanations
- 🧩 [Node.js basic example](../../nodejs/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-js-node-js-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-js-node-js-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-js-node-js-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-js-node-js-footer">Blog</a>
</p>
