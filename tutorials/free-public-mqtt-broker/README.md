# Free Public MQTT Broker for Testing: Connect to broker.connectmq.com in Minutes

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-free-public-mqtt-broker-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-free-public-mqtt-broker-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

broker.connectmq.com is a free public MQTT broker for testing and learning. Here are the ports, the anonymous access rules, the limits and copy-paste examples for the CLI, Python, Node.js and the browser.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-free-public-mqtt-broker-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-free-public-mqtt-broker-intro)

📖 **Full step-by-step tutorial:** [Free Public MQTT Broker for Testing: Connect to broker.connectmq.com in Minutes](https://connectmq.com/blog/free-public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-free-public-mqtt-broker-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-free-public-mqtt-broker-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`commands.sh`](commands.sh) | Mosquitto CLI commands: subscribe/publish, TLS, retained message and Last Will demos. |
| [`public_broker.py`](public_broker.py) | paho-mqtt 2.x client: connects over TLS (8883), subscribes to its prefix and publishes one reading. |
| [`requirements.txt`](requirements.txt) | Python dependency (`paho-mqtt>=2.0`). |
| [`node-client.js`](node-client.js) | MQTT.js v5 client over `mqtts://` (or `wss://`): subscribes and publishes one reading. |
| [`browser.js`](browser.js) | Browser module over `wss://…:8084/mqtt` that prints received messages into the page (bundle with Vite, webpack or esbuild). |
| [`package.json`](package.json) | Node.js dependency (`mqtt` v5). |

Connection details: TCP `1883`, TLS `8883`, WebSocket `8083` (`/mqtt`), Secure WebSocket `8084` (`/mqtt`). No username or password; use a non-empty, unique client ID. Limits: 64 KB per message, 10 messages/s and 10 subscriptions per client, 8 topic levels.

## Requirements

- Mosquitto command-line clients (`mosquitto_sub`, `mosquitto_pub`) and `openssl` for the CLI demo
- Python 3 with `paho-mqtt` 2.x for the Python example
- Node.js with MQTT.js v5 for the Node.js example
- A bundler (Vite, webpack or esbuild) for the browser example

## Run it on the free public broker

1. Generate a random ID and open two terminals (all CLI commands are in [`commands.sh`](commands.sh)):

   ```bash
   export ID=demo-$(openssl rand -hex 3)
   echo $ID   # e.g. demo-7f3a91

   # Terminal 1
   mosquitto_sub -h broker.connectmq.com -p 1883 -i $ID-sub -t "connectmq/demo/$ID/#" -v

   # Terminal 2
   mosquitto_pub -h broker.connectmq.com -p 1883 -i $ID-pub -t "connectmq/demo/$ID/temperature" -m '{"value": 22.5, "unit": "C"}'
   ```

2. Python:

   ```bash
   pip install "paho-mqtt>=2.0"
   python public_broker.py
   ```

3. Node.js:

   ```bash
   npm install mqtt
   node node-client.js
   ```

4. Browser: import `browser.js` from a page and bundle it with your favourite tool. Pages served over HTTPS must use `wss://` on port 8084.

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-free-public-mqtt-broker-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-free-public-mqtt-broker-private) — the **Serverless (Free)** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. Keep the same code and add the username, password and client ID from the portal. In `public_broker.py`, the post's version:

   ```python
   client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="YOUR_CLIENT_ID", protocol=mqtt.MQTTv5)
   client.username_pw_set("YOUR_USERNAME", "YOUR_PASSWORD")
   client.tls_set()
   client.connect("broker.connectmq.com", 8883)
   ```

   In `node-client.js` and `browser.js`, pass `username: "YOUR_USERNAME"`, `password: "YOUR_PASSWORD"` and `clientId: "YOUR_CLIENT_ID"` in the `mqtt.connect()` options, and keep `mqtts://…:8883` or `wss://…:8084/mqtt`. For the CLI, add `-u YOUR_USERNAME -P YOUR_PASSWORD -i YOUR_CLIENT_ID` and use port 8883 with `--capath`/`--cafile`.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [Free Public MQTT Broker for Testing: Connect to broker.connectmq.com in Minutes](https://connectmq.com/blog/free-public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-free-public-mqtt-broker-related) — the full tutorial with explanations
- 🧩 [CLI basic example](../../cli/) · [Python basic example](../../python/) · [Node.js basic example](../../nodejs/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-free-public-mqtt-broker-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-free-public-mqtt-broker-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-free-public-mqtt-broker-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-free-public-mqtt-broker-footer">Blog</a>
</p>
