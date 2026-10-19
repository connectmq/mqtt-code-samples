# Node-RED MQTT Example

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=node-red-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=node-red-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../LICENSE)

Connect Node-RED to an MQTT broker with an importable flow. Start on the free public broker, then point the same code at a secure private broker on ConnectMQ.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=node-red-intro)** — the managed, serverless MQTT broker for IoT. Try this example on the free public broker in seconds, then move the very same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=node-red-intro)

Full walkthrough on the website: **[Node-RED MQTT example](https://connectmq.com/code-samples/node-red/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=node-red-intro)**

## Requirements

- **Library:** [mqtt in / mqtt out nodes](https://nodered.org/docs/user-guide/messages)


## Files

| Folder | Broker | What it does |
| --- | --- | --- |
| [`public-broker/`](public-broker/) | Free public broker `broker.connectmq.com` | Connect without an account, subscribe and publish a JSON reading |
| [`private-broker/`](private-broker/) | Your private ConnectMQ broker | The same flow over TLS with your username and password |

## How to run

1. In Node-RED open **Menu → Import**, paste `flow.json` and click **Deploy**.
2. Watch the readings arrive in the **Debug** sidebar.

---

## 1. Try it on the free public broker (no account needed)

No account needed: connect to broker.connectmq.com on port 1883 and start publishing in seconds.

| Protocol | URL |
| --- | --- |
| MQTT (TCP) | `mqtt://broker.connectmq.com:1883` |
| MQTT over TLS | `mqtts://broker.connectmq.com:8883` |
| WebSocket | `ws://broker.connectmq.com:8083/mqtt` |
| Secure WebSocket | `wss://broker.connectmq.com:8084/mqtt` |

**`flow.json`** ([open file](public-broker/flow.json))

```json
[
  { "id": "cmq_broker", "type": "mqtt-broker", "name": "ConnectMQ broker",
    "broker": "broker.connectmq.com", "port": "1883", "usetls": false,
    "protocolVersion": "4", "keepalive": "60", "cleansession": true },
  { "id": "cmq_inject", "type": "inject", "name": "Send a reading every 10 s", "x": 160, "y": 80,
    "props": [{ "p": "payload" }], "payload": "{\"temperature\":21.5}", "payloadType": "json",
    "repeat": "10", "once": true, "wires": [["cmq_out"]] },
  { "id": "cmq_out", "type": "mqtt out", "name": "Publish a JSON reading", "x": 420, "y": 80,
    "topic": "your-project/sensors/temperature", "qos": "1", "retain": "false",
    "broker": "cmq_broker", "wires": [] },
  { "id": "cmq_in", "type": "mqtt in", "name": "Subscribe to the temperature topic", "x": 160, "y": 160,
    "topic": "your-project/sensors/#", "qos": "1", "datatype": "auto-detect",
    "broker": "cmq_broker", "wires": [["cmq_debug"]] },
  { "id": "cmq_debug", "type": "debug", "name": "Runs for every message on a subscribed topic", "x": 420, "y": 160,
    "active": true, "complete": "payload", "wires": [] }
]
```

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic, including yours. Never send passwords, personal data or anything confidential through it, and use a unique topic prefix (`your-project/...`) so your messages don't mix with others'. There is no guarantee of availability or message retention. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=node-red-public)

## 2. Go to production with a private ConnectMQ broker

For real devices, use a private serverless MQTT broker on ConnectMQ instead of the public one: TLS encryption, a username and password for every device and per-topic access control, fully managed. The Serverless (Free) plan needs no credit card.

**Get your private broker in under a minute:**

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=node-red-private) — no credit card.
2. Create a broker in the dashboard (the **Serverless (Free)** plan is enough to start).
3. Copy the **host**, **username** and **password** of your broker.
4. Replace `YOUR_BROKER_HOST`, `YOUR_USERNAME` and `YOUR_PASSWORD` in the files under [`private-broker/`](private-broker/) and run them.

**`flow.json`** ([open file](private-broker/flow.json))

```json
[
  { "id": "cmq_tls", "type": "tls-config", "name": "TLS: the system CA store verifies the broker certificate", "verifyservercert": true },
  { "id": "cmq_broker", "type": "mqtt-broker", "name": "ConnectMQ broker",
    "broker": "YOUR_BROKER_HOST", "port": "8883", "usetls": true, "tls": "cmq_tls",
    "protocolVersion": "4", "keepalive": "60", "cleansession": true,
    "credentials": { "user": "YOUR_USERNAME", "password": "YOUR_PASSWORD" } },
  { "id": "cmq_inject", "type": "inject", "name": "Send a reading every 10 s", "x": 160, "y": 80,
    "props": [{ "p": "payload" }], "payload": "{\"temperature\":21.5}", "payloadType": "json",
    "repeat": "10", "once": true, "wires": [["cmq_out"]] },
  { "id": "cmq_out", "type": "mqtt out", "name": "Publish a JSON reading", "x": 420, "y": 80,
    "topic": "your-project/sensors/temperature", "qos": "1", "retain": "false",
    "broker": "cmq_broker", "wires": [] },
  { "id": "cmq_in", "type": "mqtt in", "name": "Subscribe to the temperature topic", "x": 160, "y": 160,
    "topic": "your-project/sensors/#", "qos": "1", "datatype": "auto-detect",
    "broker": "cmq_broker", "wires": [["cmq_debug"]] },
  { "id": "cmq_debug", "type": "debug", "name": "Runs for every message on a subscribed topic", "x": 420, "y": 160,
    "active": true, "complete": "payload", "wires": [] }
]
```

### What you get with a private broker

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Devices & connections dashboard** — live device status, last values, connection history
- ⚡ **Fully managed and serverless** — no servers to patch or scale

## Public vs. private broker

| | Free public broker | Private broker on ConnectMQ |
| --- | --- | --- |
| Account | Not needed | Free sign-up, no credit card |
| Host | `broker.connectmq.com` | Your own broker host |
| Who can read your topics | **Anyone** | Only your devices |
| Encryption | Optional (TLS on 8883) | TLS on every connection |
| Authentication | None | Username and password per device |
| Topic access control (ACL) | No | Yes, per topic and per client |
| Device & connection dashboard | No | Yes |
| Use it for | Learning, demos, quick tests | Real devices and production |

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=node-red-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=node-red-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=node-red-footer">Pricing</a> ·
  <a href="https://connectmq.com/code-samples/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=node-red-footer">All code samples</a>
</p>
