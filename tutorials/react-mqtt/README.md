# React MQTT Tutorial: A Hooks-Based Real-Time Dashboard

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-react-mqtt-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-react-mqtt-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Create a reusable useMqtt hook around MQTT.js, connect React to a broker over secure WebSocket, and render live sensor values without re-render storms, StrictMode surprises or leaked connections.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-react-mqtt-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-react-mqtt-intro)

📖 **Full step-by-step tutorial:** [React MQTT Tutorial: A Hooks-Based Real-Time Dashboard](https://connectmq.com/blog/react-mqtt/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-react-mqtt-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-react-mqtt-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`src/useMqtt.js`](src/useMqtt.js) | Reusable hook around MQTT.js: connects in `useEffect`, subscribes on connect, buffers messages and flushes them to state every 250 ms, exposes `status`, `messages` and `publish` |
| [`src/App.jsx`](src/App.jsx) | Live sensor dashboard with one card per device, data-age indicator and a "Toggle fan1" command button (with the post's stable-`clientId` fix applied) |
| [`src/MqttContext.jsx`](src/MqttContext.jsx) | `MqttProvider` / `useMqttContext` to share one connection across many components |

These files go into the `src/` folder of a Vite React project (see below). Add some minimal CSS to `src/index.css` for the `.grid` and `.card` classes, or use your component library of choice.

## Requirements

- Node.js and npm
- A Vite React project
- [MQTT.js](https://github.com/mqttjs/MQTT.js) v5 (`mqtt` package)
- `mosquitto_pub` / `mosquitto_sub` to feed test data

## Run it on the free public broker

Browsers cannot open raw TCP sockets, so the app connects over secure WebSocket: `wss://broker.connectmq.com:8084/mqtt`.

1. Create a Vite React project and install MQTT.js, then copy the `src/` files from this folder into it:

   ```bash
   npm create vite@latest react-mqtt-dashboard -- --template react
   cd react-mqtt-dashboard
   npm install
   npm install mqtt
   npm run dev
   ```

2. Feed it test data (use your own random prefix — the public area is readable by everyone):

   ```bash
   for i in $(seq 1 30); do
     mosquitto_pub -h broker.connectmq.com -p 1883 -i react-pub-58d2 \
       -t connectmq/demo/react-58d2/room1/telemetry \
       -m "{\"temperature\": $((20 + RANDOM % 5)), \"humidity\": $((40 + RANDOM % 10))}"
     sleep 1
   done
   ```

3. Click **Toggle fan1** and watch the command arrive:

   ```bash
   mosquitto_sub -h broker.connectmq.com -p 1883 -i react-sub-58d2 -v -t "connectmq/demo/react-58d2/+/cmd"
   ```

To share one connection across components, wrap your app in `<MqttProvider url={BROKER_URL} topics={[...]}>` and call `useMqttContext()` anywhere below it.

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-react-mqtt-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-react-mqtt-private) — the **Free** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. In `src/App.jsx`, point the hook at your broker's secure WebSocket URL and pass the credentials (for example from `.env` as `VITE_MQTT_USERNAME` / `VITE_MQTT_PASSWORD`):

   ```javascript
   const { status, messages } = useMqtt(
     "wss://YOUR_BROKER_HOST:8084/mqtt",
     { clientId, username: import.meta.env.VITE_MQTT_USERNAME, password: import.meta.env.VITE_MQTT_PASSWORD },
     ["factory1/+/telemetry"]
   );
   ```

   Credentials in the browser are public: issue a dedicated credential for the dashboard, and route commands through a backend API if users must not publish. Each tab needs a unique client ID.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [React MQTT Tutorial: A Hooks-Based Real-Time Dashboard](https://connectmq.com/blog/react-mqtt/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-react-mqtt-related) — the full tutorial with explanations
- 🧩 [Node.js basic example](../../nodejs/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-react-mqtt-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-react-mqtt-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-react-mqtt-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-react-mqtt-footer">Blog</a>
</p>
