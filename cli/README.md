# CLI (mosquitto) MQTT Example

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=cli-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=cli-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../LICENSE)

Publish and subscribe from the command line with mosquitto_pub and mosquitto_sub. Start on the free public broker, then point the same code at a secure private broker on ConnectMQ.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=cli-intro)** — the managed, serverless MQTT broker for IoT. Try this example on the free public broker in seconds, then move the very same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=cli-intro)

Full walkthrough on the website: **[CLI (mosquitto) MQTT example](https://connectmq.com/code-samples/cli/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=cli-intro)**

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=cli-hero"><img src="../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## Requirements

- **Library:** [mosquitto_pub / mosquitto_sub](https://mosquitto.org/download/)
- **Install:**

```bash
# macOS: brew install mosquitto  ·  Debian/Ubuntu: sudo apt install mosquitto-clients
```

## Files

| Folder | Broker | What it does |
| --- | --- | --- |
| [`public-broker/`](public-broker/) | Free public broker `broker.connectmq.com` | Connect without an account, subscribe and publish a JSON reading |
| [`private-broker/`](private-broker/) | Your private ConnectMQ broker | The same flow over TLS with your username and password |

## How to run

1. Install the mosquitto clients: `brew install mosquitto` (macOS) or `sudo apt install mosquitto-clients` (Debian / Ubuntu).
2. Run the `mosquitto_sub` command in one terminal and the `mosquitto_pub` command in another.

---

## 1. Try it on the free public broker (no account needed)

No account needed: connect to broker.connectmq.com on port 1883 and start publishing in seconds.

| Protocol | URL |
| --- | --- |
| MQTT (TCP) | `mqtt://broker.connectmq.com:1883` |
| MQTT over TLS | `mqtts://broker.connectmq.com:8883` |
| WebSocket | `ws://broker.connectmq.com:8083/mqtt` |
| Secure WebSocket | `wss://broker.connectmq.com:8084/mqtt` |

**Terminal — `commands.sh`** ([open file](public-broker/commands.sh))

```bash
# Subscribe to the temperature topic
mosquitto_sub -h broker.connectmq.com -p 1883 -t "your-project/sensors/#" -v

# Publish a JSON reading
mosquitto_pub -h broker.connectmq.com -p 1883 -t "your-project/sensors/temperature" -m '{"temperature":21.5}'
```

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic, including yours. Never send passwords, personal data or anything confidential through it, and use a unique topic prefix (`your-project/...`) so your messages don't mix with others'. There is no guarantee of availability or message retention. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=cli-public)

## 2. Go to production with a private ConnectMQ broker

For real devices, use a private serverless MQTT broker on ConnectMQ instead of the public one: TLS encryption, a username and password for every device and per-topic access control, fully managed. The Free plan needs no credit card.

**Get your private broker in under a minute:**

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=cli-private) — no credit card.
2. Create a broker in the dashboard (the **Free** plan is enough to start).
3. Copy the **host**, **username** and **password** of your broker.
4. Replace `YOUR_BROKER_HOST`, `YOUR_USERNAME` and `YOUR_PASSWORD` in the files under [`private-broker/`](private-broker/) and run them.

**Terminal — `commands.sh`** ([open file](private-broker/commands.sh))

```bash
# Subscribe to the temperature topic (TLS: the system CA store verifies the broker certificate)
mosquitto_sub -h YOUR_BROKER_HOST -p 8883 --capath /etc/ssl/certs \
  -u YOUR_USERNAME -P YOUR_PASSWORD -t "your-project/sensors/#" -v

# Publish a JSON reading
mosquitto_pub -h YOUR_BROKER_HOST -p 8883 --capath /etc/ssl/certs \
  -u YOUR_USERNAME -P YOUR_PASSWORD -t "your-project/sensors/temperature" -m '{"temperature":21.5}'
```

### What you get with a private broker

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Devices & connections dashboard** — live device status, last values, connection history
- ⚡ **Fully managed and serverless** — no servers to patch or scale

<table>
  <tr>
    <td width="50%" valign="top"><a href="https://connectmq.com/monitoring/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=cli-gallery"><img src="../assets/dashboard.png" alt="ConnectMQ dashboard: broker status, ISA-95 topic tree and live value cards with sparklines for every topic" width="100%"></a><br><b>Live dashboard</b> — broker status, ISA-95 topic tree and a live card for every topic</td>
    <td width="50%" valign="top"><a href="https://connectmq.com/digital-twin/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=cli-gallery"><img src="../assets/digital-twin.png" alt="ConnectMQ 3D Digital Twin: machines bound to their MQTT topics with live telemetry" width="100%"></a><br><b>3D Digital Twin</b> — machines bound to their MQTT topics, telemetry on the equipment</td>
  </tr>
  <tr>
    <td width="50%" valign="top"><a href="https://connectmq.com/rules-alerts/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=cli-gallery"><img src="../assets/rules.png" alt="ConnectMQ alert rules: conditions on JSON payload fields with message templates" width="100%"></a><br><b>Rules</b> — thresholds on JSON payload fields, such as <code>{temp} &gt; 70</code></td>
    <td width="50%" valign="top"><a href="https://connectmq.com/rules-alerts/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=cli-gallery"><img src="../assets/alerts.png" alt="ConnectMQ triggered alerts: audit log with the exact payload that caused each alert" width="100%"></a><br><b>Alerts</b> — audit log with the exact payload, plus browser notifications</td>
  </tr>
</table>

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
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=cli-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=cli-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=cli-footer">Pricing</a> ·
  <a href="https://connectmq.com/code-samples/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=cli-footer">All code samples</a>
</p>
