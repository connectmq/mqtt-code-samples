# Build a Real-Time MQTT Chat App with JavaScript, Presence and No Local

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-chat-app-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-chat-app-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Build a browser chat app on MQTT over secure WebSocket, with rooms, retained presence that survives crashes via Last Will, and the MQTT 5 No Local option, running on broker.connectmq.com.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-chat-app-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-chat-app-intro)

📖 **Full step-by-step tutorial:** [Build a Real-Time MQTT Chat App with JavaScript, Presence and No Local](https://connectmq.com/blog/mqtt-chat-app/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-chat-app-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-chat-app-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`chat.html`](chat.html) | Complete browser chat in one file: MQTT.js over secure WebSocket (8084), rooms as topics, retained presence with a Last Will for crashes, and the MQTT 5 No Local option so your own messages are not echoed back |

## Requirements

- A modern web browser (MQTT.js 5.10.1 is loaded from unpkg)
- Optionally, `mosquitto_sub` to watch the raw traffic

## Run it on the free public broker

1. Open `chat.html` and change `PREFIX` to your own random string, shared by everyone who should see the chat:

   ```js
   const PREFIX = "connectmq/demo/chat-k7f3q2";
   ```

2. Open `chat.html` in two browser windows (or send the file to a friend), enter different names and the same room, and start chatting.
3. Watch the raw traffic from a terminal — the retained presence messages first, then chat messages as they arrive:

   ```bash
   mosquitto_sub -h broker.connectmq.com -p 1883 -i chat-watch-9c1e -t 'connectmq/demo/chat-k7f3q2/#' -v
   ```

Testing checklist from the tutorial: both names appear in each user list; each message appears exactly once on both sides; closing a window removes the name immediately; disconnecting the network shows the user offline after about 30 seconds.

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-chat-app-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-chat-app-private) — the **Free** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. In `chat.html`, point `URL` at your broker's secure WebSocket endpoint and add the credentials to the `mqtt.connect` options (the page already marks the spot with a comment):

   ```js
   const URL = "wss://YOUR_BROKER_HOST:8084/mqtt";
   ```

   ```js
   client = mqtt.connect(URL, {
     clientId,
     protocolVersion: 5,
     // ...
     username: "YOUR_USERNAME",
     password: "YOUR_PASSWORD"
   });
   ```

   Browser code is visible to its users, so think about where those credentials live before sharing the page beyond a demo.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [Build a Real-Time MQTT Chat App with JavaScript, Presence and No Local](https://connectmq.com/blog/mqtt-chat-app/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-chat-app-related) — the full tutorial with explanations
- 🧩 [Node.js basic example](../../nodejs/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-chat-app-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-chat-app-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-chat-app-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-chat-app-footer">Blog</a>
</p>
