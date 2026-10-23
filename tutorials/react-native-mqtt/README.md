# React Native MQTT: Real-Time Mobile IoT Apps over WebSocket

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-react-native-mqtt-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-react-native-mqtt-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Build a React Native MQTT app with MQTT.js over secure WebSocket: a reusable hook, live device data, commands, and correct reconnect handling when the app moves between background and foreground.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-react-native-mqtt-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-react-native-mqtt-intro)

📖 **Full step-by-step tutorial:** [React Native MQTT: Real-Time Mobile IoT Apps over WebSocket](https://connectmq.com/blog/react-native-mqtt/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-react-native-mqtt-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-react-native-mqtt-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`hooks/useMqtt.js`](hooks/useMqtt.js) | Reusable hook: connects with MQTT.js over `wss://…:8084/mqtt`, subscribes on connect, exposes status, messages and `publish`, and disconnects on `background` / reconnects on `active` |
| [`app/index.js`](app/index.js) | `DeviceScreen` showing tank level and pump status, with a switch that publishes `ON`/`OFF` pump commands |

Copy these into an Expo project. Load the URL polyfill once at the very top of your entry file (`app/_layout.tsx` in Expo Router, or `index.js` in a bare app):

```javascript
import "react-native-url-polyfill/auto";
```

## Requirements

- Node.js and an Expo (or bare React Native) project
- [MQTT.js](https://github.com/mqttjs/MQTT.js) v5 (`mqtt` package)
- `react-native-url-polyfill`
- Expo Go or a device/simulator; `mosquitto_pub` / `mosquitto_sub` to simulate the device

## Run it on the free public broker

1. Create the project and install the dependencies:

   ```bash
   npx create-expo-app@latest mqtt-demo
   cd mqtt-demo
   npx expo install react-native-url-polyfill
   npm install mqtt
   ```

   If Metro resolves the Node build of MQTT.js (errors about `net`, `tls` or `fs`), import the bundle explicitly with `import mqtt from "mqtt/dist/mqtt.esm"`.

2. Start the app, then simulate the tank and pump from a terminal (keep a random prefix — the public area is readable by everyone):

   ```bash
   PREFIX="connectmq/demo/rn-7f3a91"

   # Retained so the app sees it immediately after connecting
   mosquitto_pub -h broker.connectmq.com -p 1883 -i rn-sim-tank -r \
     -t "$PREFIX/tank/level" -m "64"

   mosquitto_pub -h broker.connectmq.com -p 1883 -i rn-sim-pump -r \
     -t "$PREFIX/pump/status" -m "OFF"

   mosquitto_sub -h broker.connectmq.com -p 1883 -i rn-sim-cmd -t "$PREFIX/pump/set" -v
   ```

3. Flip the pump switch and watch `ON`/`OFF` arrive in `mosquitto_sub`. Background the app for a minute, bring it back, and confirm the status goes from `connecting` to `connected` and the retained values reappear instantly.

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-react-native-mqtt-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-react-native-mqtt-private) — the **Free** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. In `hooks/useMqtt.js`, set `BROKER_URL` to `wss://YOUR_BROKER_HOST:8084/mqtt`, then pass the credentials to the hook in `app/index.js`:

   ```javascript
   useMqtt({ topics, username: "YOUR_USERNAME", password: "YOUR_PASSWORD", clientId: "YOUR_CLIENT_ID" })
   ```

   Store secrets with `expo-secure-store` or the platform keychain, never in the JavaScript bundle. ConnectMQ binds client IDs to issued credentials, so for a multi-user app have your backend hand each user their own credentials after login.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [React Native MQTT: Real-Time Mobile IoT Apps over WebSocket](https://connectmq.com/blog/react-native-mqtt/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-react-native-mqtt-related) — the full tutorial with explanations
- 🧩 [Node.js basic example](../../nodejs/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-react-native-mqtt-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-react-native-mqtt-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-react-native-mqtt-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-react-native-mqtt-footer">Blog</a>
</p>
