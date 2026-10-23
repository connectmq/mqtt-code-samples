# iOS MQTT Swift Client with CocoaMQTT and SwiftUI

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-ios-mqtt-swift-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-ios-mqtt-swift-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Step-by-step iOS MQTT Swift tutorial: add CocoaMQTT with Swift Package Manager, wrap it in an ObservableObject, show live sensor data in SwiftUI and publish commands over TLS.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-ios-mqtt-swift-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-ios-mqtt-swift-intro)

📖 **Full step-by-step tutorial:** [iOS MQTT Swift Client with CocoaMQTT and SwiftUI](https://connectmq.com/blog/ios-mqtt-swift/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-ios-mqtt-swift-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-ios-mqtt-swift-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`MQTTModel.swift`](MQTTModel.swift) | `ObservableObject` that owns the CocoaMQTT client: TLS connect, auto-reconnect, subscribes to `<prefix>/sensors/+/temperature` and publishes `ON`/`OFF` to `<prefix>/fan/set` |
| [`ContentView.swift`](ContentView.swift) | SwiftUI screen showing connection state, live sensor readings and a fan toggle; reconnects on `scenePhase` changes |

## Requirements

- Xcode 15 or newer and an iOS 16+ simulator or device (the two-parameter `onChange` used in `ContentView.swift` requires iOS 17; on iOS 16 use the single-parameter closure)
- The [CocoaMQTT](https://github.com/emqx/CocoaMQTT) package (Swift Package Manager, "Up to Next Major Version" from 2.1.0)
- Optionally, the Mosquitto CLI tools (`mosquitto_pub` / `mosquitto_sub`) to simulate a device

## Run it on the free public broker

1. Create a new iOS app in Xcode. Choose **File → Add Package Dependencies**, enter the URL below, select "Up to Next Major Version" from 2.1.0 and add the `CocoaMQTT` library to your app target:

   ```text
   https://github.com/emqx/CocoaMQTT.git
   ```

2. Add `MQTTModel.swift` and `ContentView.swift` to the target. No App Transport Security exception is needed: the app connects over TLS (port 8883) to `broker.connectmq.com`, which uses a publicly trusted certificate.
3. Run the app and copy the topic prefix shown on the screen (a random `connectmq/demo/<id>`).
4. Publish simulated readings and watch the fan commands from a terminal:

   ```bash
   PREFIX="connectmq/demo/1a2b3c4d"   # paste the prefix shown in the app

   mosquitto_pub -h broker.connectmq.com -p 1883 -i ios-sim-kitchen \
     -t "$PREFIX/sensors/kitchen/temperature" -m "22.8"

   mosquitto_pub -h broker.connectmq.com -p 1883 -i ios-sim-office \
     -t "$PREFIX/sensors/office/temperature" -m "20.1"

   # Watch fan commands from the app
   mosquitto_sub -h broker.connectmq.com -p 1883 -i ios-sim-fan -t "$PREFIX/fan/set" -v
   ```

   Both sensors appear in the list, and toggling the fan prints `ON` or `OFF` in the subscriber.

If port 8883 is blocked on your network, CocoaMQTT can tunnel MQTT through secure WebSocket on port 8084:

```swift
let websocket = CocoaMQTTWebSocket(uri: "/mqtt")
let client = CocoaMQTT(clientID: id, host: "broker.connectmq.com", port: 8084, socket: websocket)
client.enableSSL = true
```

To publish the app's own online status, set a last will in the model's initializer before `connect()` is called:

```swift
mqtt.willMessage = CocoaMQTTMessage(topic: "\(self.topicPrefix)/apps/\(id)/status",
                                    string: "offline", qos: .qos1, retained: true)
```

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-ios-mqtt-swift-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-ios-mqtt-swift-private) — the **Free** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. Initialise the model in `ContentView.swift` with your broker's host and credentials instead of `MQTTModel()`, and keep `enableSSL = true` on port 8883:

   ```swift
   @StateObject private var model = MQTTModel(host: "YOUR_BROKER_HOST",
                                              username: "YOUR_USERNAME",
                                              password: "YOUR_PASSWORD",
                                              clientID: "YOUR_CLIENT_ID",
                                              topicPrefix: "acme/home1")
   ```

   Store the password in the Keychain, not in `UserDefaults` or source code. For App Store apps, avoid one shared login in every installed copy: let a backend issue per-user or per-device MQTT credentials over HTTPS.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [iOS MQTT Swift Client with CocoaMQTT and SwiftUI](https://connectmq.com/blog/ios-mqtt-swift/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-ios-mqtt-swift-related) — the full tutorial with explanations
- 🧩 [Swift and Kotlin basic examples](../../swift-kotlin/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-ios-mqtt-swift-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-ios-mqtt-swift-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-ios-mqtt-swift-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-ios-mqtt-swift-footer">Blog</a>
</p>
