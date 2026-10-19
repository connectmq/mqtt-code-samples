# MQTT Code Samples by ConnectMQ

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=root-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=root-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

Ready-to-run MQTT examples for **12 languages and platforms**: connect, subscribe and publish a JSON sensor reading in a few lines of code.

Every example comes in two versions:

1. **`public-broker/`** — runs right away on the free public broker `broker.connectmq.com`, no account needed.
2. **`private-broker/`** — the same code on a secure private broker on **[ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=root-intro)**: TLS, a username and password per device and per-topic access control.

> **[ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=root-intro)** is a managed, serverless MQTT broker for IoT devices, apps and digital twins. Start on the **Serverless (Free)** plan — no credit card. 👉 **[Create your free broker](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=root-intro)**

## Examples

| Language / platform | Library | Step-by-step guide |
| --- | --- | --- |
| [Python](python/) | paho-mqtt 2.x | [Guide](https://connectmq.com/code-samples/python/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=root-python) |
| [Node.js](nodejs/) | MQTT.js 5 | [Guide](https://connectmq.com/code-samples/nodejs/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=root-nodejs) |
| [ESP32](esp32/) | PubSubClient (Arduino) | [Guide](https://connectmq.com/code-samples/esp32/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=root-esp32) |
| [Go](go/) | Eclipse Paho Go | [Guide](https://connectmq.com/code-samples/go/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=root-go) |
| [CLI (mosquitto)](cli/) | mosquitto_pub / mosquitto_sub | [Guide](https://connectmq.com/code-samples/cli/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=root-cli) |
| [Java](java/) | Eclipse Paho Java Client | [Guide](https://connectmq.com/code-samples/java/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=root-java) |
| [C# (.NET)](csharp/) | MQTTnet 4 | [Guide](https://connectmq.com/code-samples/csharp/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=root-csharp) |
| [Rust](rust/) | rumqttc | [Guide](https://connectmq.com/code-samples/rust/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=root-rust) |
| [Dart (Flutter)](dart-flutter/) | mqtt_client | [Guide](https://connectmq.com/code-samples/dart-flutter/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=root-dart-flutter) |
| [Swift / Kotlin](swift-kotlin/) | CocoaMQTT (iOS) · HiveMQ MQTT Client (Android) | [Guide](https://connectmq.com/code-samples/swift-kotlin/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=root-swift-kotlin) |
| [Home Assistant](home-assistant/) | MQTT integration | [Guide](https://connectmq.com/code-samples/home-assistant/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=root-home-assistant) |
| [Node-RED](node-red/) | mqtt in / mqtt out nodes | [Guide](https://connectmq.com/code-samples/node-red/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=root-node-red) |

Each folder has its own README with install steps, both code versions and how to run them.

## Quick start: the free public broker

No sign-up, no setup — point any MQTT client at it:

| Protocol | URL |
| --- | --- |
| MQTT (TCP) | `mqtt://broker.connectmq.com:1883` |
| MQTT over TLS | `mqtts://broker.connectmq.com:8883` |
| WebSocket | `ws://broker.connectmq.com:8083/mqtt` |
| Secure WebSocket | `wss://broker.connectmq.com:8084/mqtt` |

Supports MQTT 3.1.1 and MQTT 5.

```bash
# Terminal 1: subscribe
mosquitto_sub -h broker.connectmq.com -p 1883 -t "your-project/sensors/#" -v

# Terminal 2: publish
mosquitto_pub -h broker.connectmq.com -p 1883 -t "your-project/sensors/temperature" -m '{"temperature":21.5}'
```

> ⚠️ The public broker is **shared**: anyone can subscribe to any topic. Use a unique topic prefix, never send confidential data, and expect no availability guarantee. [Learn more](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=root-public)

## Going to production: your private ConnectMQ broker

When your devices leave the desk, switch to a private broker — only the host, port and credentials change:

1. **[Sign up for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=root-private)** (no credit card).
2. **Create a broker** in the dashboard and copy its host, username and password.
3. Open the `private-broker/` file of your language, replace `YOUR_BROKER_HOST`, `YOUR_USERNAME` and `YOUR_PASSWORD`, and run it.

What you get:

- 🔒 **TLS** on every connection
- 🔑 **Per-device credentials**
- 🛡️ **Topic access control (ACL)** — per topic, per client, with `${clientid}` / `${username}` placeholders
- 📊 **Device dashboard** — live status, last values and connection history of every device
- ⚡ **Serverless & fully managed** — scale from one sensor to a fleet without running servers

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

## Contributing

Found a bug or want an example for another language? [Open an issue](../../issues) or send a pull request.

## License

[MIT](LICENSE) — use these examples freely in your own projects, commercial or not.

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=root-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=root-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=root-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=root-footer">Blog</a>
</p>
