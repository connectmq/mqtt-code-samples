# MQTT Client Libraries: Choosing the Right One for Every Language

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-client-libraries-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-client-libraries-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

A practical comparison of maintained MQTT client libraries for Python, JavaScript, Go, Java, C#, Rust, C, embedded and mobile, with a minimal connect-and-publish snippet for each one, tested against broker.connectmq.com.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-client-libraries-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-client-libraries-intro)

📖 **Full step-by-step tutorial:** [MQTT Client Libraries: Choosing the Right One for Every Language](https://connectmq.com/blog/mqtt-client-libraries/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-client-libraries-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-client-libraries-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

One minimal connect / subscribe / publish program per library, all talking to `connectmq/demo/k3x8p1/libs/<language>`:

| File | What it does |
| --- | --- |
| [`python/libs_python.py`](python/libs_python.py) | paho-mqtt 2.x (MQTT 5, TLS on 8883): subscribes and publishes in `on_connect`, prints incoming messages |
| [`javascript/libs.mjs`](javascript/libs.mjs) | MQTT.js 5.x in Node.js (`mqtts://` on 8883, MQTT 5) using `subscribeAsync` / `publishAsync` |
| [`go/main.go`](go/main.go) | Eclipse Paho Go (`paho.mqtt.golang`, MQTT 3.1.1) over TLS with auto-reconnect |
| [`java/LibsJava.java`](java/LibsJava.java) | Eclipse Paho Java `mqttv3` client over `ssl://` with automatic reconnect |
| [`csharp/Program.cs`](csharp/Program.cs) | MQTTnet 5 top-level program: MQTT 5 over TLS, subscribe and publish |
| [`rust/src/main.rs`](rust/src/main.rs) | rumqttc async client on tokio (plain TCP 1883), polling the event loop |
| [`c/main.c`](c/main.c) | Eclipse Paho C synchronous client (TCP 1883): publish one QoS 1 message |

## Requirements

Only the toolchain for the language you want to try:

- **Python:** Python 3 and `paho-mqtt` 2.x
- **JavaScript:** Node.js and MQTT.js 5.x (`mqtt`)
- **Go:** Go and `github.com/eclipse/paho.mqtt.golang`
- **Java:** a JDK and Eclipse Paho `org.eclipse.paho.client.mqttv3`
- **C#:** .NET and MQTTnet 5 (version 4 uses `MqttFactory` instead of `MqttClientFactory`)
- **Rust:** Rust with `rumqttc` and `tokio` (TLS needs one of rumqttc's TLS feature flags)
- **C:** Eclipse Paho C (`MQTTClient.h`, synchronous library)

## Run it on the free public broker

Every program connects anonymously to `broker.connectmq.com`, so run any one of them as-is with your language's usual tooling (for example `python python/libs_python.py` or `node javascript/libs.mjs` after installing the library). Change the `k3x8p1` part of the topic to your own random string.

To compare libraries side by side, run one program as a subscriber and publish from another language, or watch everything with the Mosquitto CLI:

```bash
mosquitto_sub -h broker.connectmq.com -p 1883 -i libs-watch-k3x8p1 -t 'connectmq/demo/k3x8p1/libs/#' -v
```

Ports: TCP 1883, TLS 8883, WebSocket 8083 and Secure WebSocket 8084 (path `/mqtt`). In the browser, MQTT.js connects to `wss://broker.connectmq.com:8084/mqtt`.

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-client-libraries-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-client-libraries-private) — the **Free** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. Switching any program is a three-line change: use the generated client ID exactly as given, set the username and password, and enable TLS on port 8883. For `python/libs_python.py`:

   ```python
   client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="YOUR_CLIENT_ID", protocol=mqtt.MQTTv5)
   client.username_pw_set("YOUR_USERNAME", "YOUR_PASSWORD")
   client.tls_set()
   ```

   and replace `broker.connectmq.com` with your broker host in the `connect` call. The other languages follow the same pattern: client ID, username/password option of the library, and the TLS endpoint (`mqtts://…:8883` in MQTT.js, `tls://…:8883` in Go, `ssl://…:8883` in Paho Java, `WithTlsOptions` plus `WithCredentials` in MQTTnet; the Rust and C programs use plain TCP 1883 and need TLS enabled first).

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [MQTT Client Libraries: Choosing the Right One for Every Language](https://connectmq.com/blog/mqtt-client-libraries/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-client-libraries-related) — the full tutorial with explanations
- 🧩 Basic examples per language: [Python](../../python/) · [Node.js](../../nodejs/) · [Go](../../go/) · [Java](../../java/) · [C#](../../csharp/) · [Rust](../../rust/) · [ESP32](../../esp32/) · [Swift and Kotlin](../../swift-kotlin/) · [Dart and Flutter](../../dart-flutter/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-client-libraries-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-client-libraries-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-client-libraries-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-client-libraries-footer">Blog</a>
</p>
