# Vue MQTT Client: Real-Time Data over WebSocket with Vue 3

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-vue-mqtt-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-vue-mqtt-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Write a reusable Vue 3 composable around MQTT.js, connect to a broker over wss, and build a live sensor widget, plus the reactivity and lifecycle pitfalls that trip up most Vue MQTT apps.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-vue-mqtt-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-vue-mqtt-intro)

📖 **Full step-by-step tutorial:** [Vue MQTT Client: Real-Time Data over WebSocket with Vue 3](https://connectmq.com/blog/vue-mqtt/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-vue-mqtt-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-vue-mqtt-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`src/composables/useMqtt.js`](src/composables/useMqtt.js) | Vue 3 composable around MQTT.js: connection status, latest message per topic, publish, cleanup on unmount |
| [`src/components/SensorWidget.vue`](src/components/SensorWidget.vue) | Live sensor widget showing temperature and humidity, with a "Toggle fan" command button |
| [`src/App.vue`](src/App.vue) | Demo app that renders one `SensorWidget` for `greenhouse1` |
| [`src/composables/useSharedMqtt.js`](src/composables/useSharedMqtt.js) | Module-level singleton variant: one connection per tab, each topic subscribed once, closed by the last widget |

## Requirements

- Node.js with npm
- A Vue 3 project created with `npm create vue@latest` (Vite)
- MQTT.js v5 (`mqtt`)

## Run it on the free public broker

1. Create the project and install MQTT.js:

   ```bash
   npm create vue@latest vue-mqtt-demo
   cd vue-mqtt-demo
   npm install
   npm install mqtt
   npm run dev
   ```

2. Copy the `src/` files from this folder into the project's `src/` (replacing `App.vue`). Change the prefix `connectmq/demo/vue-c42e` in `App.vue` to your own random string.
3. Publish test readings from a terminal; the widget updates every second:

   ```bash
   for i in $(seq 1 30); do
     mosquitto_pub -h broker.connectmq.com -p 1883 -i vue-pub-c42e \
       -t connectmq/demo/vue-c42e/greenhouse1/telemetry \
       -m "{\"temperature\": $((18 + RANDOM % 8)), \"humidity\": $((55 + RANDOM % 15))}"
     sleep 1
   done
   ```

4. Press **Toggle fan** and watch the commands arrive:

   ```bash
   mosquitto_sub -h broker.connectmq.com -p 1883 -i vue-sub-c42e -v -t "connectmq/demo/vue-c42e/+/cmd"
   ```

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-vue-mqtt-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-vue-mqtt-private) — the **Serverless (Free)** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. In `src/components/SensorWidget.vue`, change the `useMqtt(...)` call to your broker's secure WebSocket URL and pass the credentials through Vite environment variables (`VITE_MQTT_USERNAME`, `VITE_MQTT_PASSWORD` in a local `.env`):

   ```javascript
   const { status, messages } = useMqtt(
     "wss://YOUR_BROKER_HOST:8084/mqtt",
     {
       clientId,
       username: import.meta.env.VITE_MQTT_USERNAME,
       password: import.meta.env.VITE_MQTT_PASSWORD,
     },
     ["factory1/+/telemetry"]
   );
   ```

   Anything bundled into frontend code can be read by users: use a dedicated dashboard credential and send sensitive commands through a backend API.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [Vue MQTT Client: Real-Time Data over WebSocket with Vue 3](https://connectmq.com/blog/vue-mqtt/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-vue-mqtt-related) — the full tutorial with explanations
- 🧩 [Node.js basic example](../../nodejs/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-vue-mqtt-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-vue-mqtt-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-vue-mqtt-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-vue-mqtt-footer">Blog</a>
</p>
