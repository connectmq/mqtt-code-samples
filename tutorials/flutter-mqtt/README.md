# Flutter MQTT Client: Building a Cross-Platform IoT App

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-flutter-mqtt-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-flutter-mqtt-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

A hands-on Flutter MQTT tutorial using the mqtt_client package to connect Android, iOS, desktop and web builds to a cloud broker over TLS or secure WebSocket, read live sensor data and control a device.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-flutter-mqtt-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-flutter-mqtt-intro)

📖 **Full step-by-step tutorial:** [Flutter MQTT Client: Building a Cross-Platform IoT App](https://connectmq.com/blog/flutter-mqtt/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-flutter-mqtt-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-flutter-mqtt-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`lib/mqtt/client_factory.dart`](lib/mqtt/client_factory.dart) | Conditional export: picks the server (TLS) or web (WSS) client factory per platform. |
| [`lib/mqtt/client_factory_server.dart`](lib/mqtt/client_factory_server.dart) | Creates an `MqttServerClient` on port 8883 with TLS (Android, iOS, desktop). |
| [`lib/mqtt/client_factory_web.dart`](lib/mqtt/client_factory_web.dart) | Creates an `MqttBrowserClient` on `wss://…/mqtt` port 8084 (Flutter web). |
| [`lib/mqtt/mqtt_service.dart`](lib/mqtt/mqtt_service.dart) | Service that connects with auto-reconnect, streams temperature readings and connection state, and publishes relay commands. |
| [`lib/main.dart`](lib/main.dart) | One-screen app: connection chip, live temperature, relay switch and the topic prefix. |

## Requirements

- Flutter SDK (Android, iOS, desktop or web target)
- The `mqtt_client` package from pub.dev (MQTT 3.1.1)
- Optional: Mosquitto command-line tools to simulate a device

## Run it on the free public broker

1. Create a Flutter project, add the package and copy the `lib/` folder into it:

   ```bash
   flutter pub add mqtt_client
   ```

2. Run the app (`flutter run`). It shows a random topic prefix on screen; copy it.
3. Act as the device from two terminals, replacing `PREFIX` with the value shown in the app:

   ```bash
   # Watch the commands the app sends
   mosquitto_sub -h broker.connectmq.com -p 1883 -i sim-sub-81723 -t "PREFIX/relay/set" -v

   # Publish a fake temperature reading every 2 seconds
   while true; do
     mosquitto_pub -h broker.connectmq.com -p 1883 -i sim-pub-81723 \
       -t "PREFIX/sensor/temperature" -m "{\"value\": $((RANDOM % 10 + 18)).$((RANDOM % 10))}"
     sleep 2
   done
   ```

4. Flip the switch in the app and watch `ON` / `OFF` arrive in the subscriber terminal.

On Android release builds add `<uses-permission android:name="android.permission.INTERNET"/>` to the main `AndroidManifest.xml`; on macOS enable `com.apple.security.network.client` in the entitlements.

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-flutter-mqtt-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-flutter-mqtt-private) — the **Serverless (Free)** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. In `lib/main.dart`, construct the service with your credentials (TLS on 8883 for native, WSS on 8084 for web are already used by the client factories; pass `host:` too if your broker host is not `broker.connectmq.com`):

   ```dart
   MqttService(username: 'YOUR_USERNAME', password: 'YOUR_PASSWORD', clientId: 'YOUR_CLIENT_ID', topicPrefix: 'acme/site1')
   ```

   Do not ship one shared password inside every copy of a public app; issue credentials per user or per device from a backend you control.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [Flutter MQTT Client: Building a Cross-Platform IoT App](https://connectmq.com/blog/flutter-mqtt/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-flutter-mqtt-related) — the full tutorial with explanations
- 🧩 [Dart / Flutter basic example](../../dart-flutter/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-flutter-mqtt-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-flutter-mqtt-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-flutter-mqtt-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-flutter-mqtt-footer">Blog</a>
</p>
