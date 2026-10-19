# Swift / Kotlin MQTT Example

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=swift-kotlin-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=swift-kotlin-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../LICENSE)

Connect native iOS (Swift) and Android (Kotlin) apps to an MQTT broker. Start on the free public broker, then point the same code at a secure private broker on ConnectMQ.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=swift-kotlin-intro)** — the managed, serverless MQTT broker for IoT. Try this example on the free public broker in seconds, then move the very same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=swift-kotlin-intro)

Full walkthrough on the website: **[Swift / Kotlin MQTT example](https://connectmq.com/code-samples/swift-kotlin/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=swift-kotlin-intro)**

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=swift-kotlin-hero"><img src="../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## Requirements

- **Library:** [CocoaMQTT (iOS) · HiveMQ MQTT Client (Android)](https://github.com/emqx/CocoaMQTT)
- **Install:**

```bash
# iOS (Swift Package Manager): https://github.com/emqx/CocoaMQTT
# Android (Gradle): implementation("com.hivemq:hivemq-mqtt-client:1.3.3")
```

## Files

| Folder | Broker | What it does |
| --- | --- | --- |
| [`public-broker/`](public-broker/) | Free public broker `broker.connectmq.com` | Connect without an account, subscribe and publish a JSON reading |
| [`private-broker/`](private-broker/) | Your private ConnectMQ broker | The same flow over TLS with your username and password |

## How to run

1. **iOS:** add [CocoaMQTT](https://github.com/emqx/CocoaMQTT) with Swift Package Manager and call the code in `MQTTExample.swift` from your app.
2. **Android:** add `implementation("com.hivemq:hivemq-mqtt-client:1.3.3")` to your Gradle file and run the code in `MqttExample.kt` (off the main thread).

---

## 1. Try it on the free public broker (no account needed)

No account needed: connect to broker.connectmq.com on port 1883 and start publishing in seconds.

| Protocol | URL |
| --- | --- |
| MQTT (TCP) | `mqtt://broker.connectmq.com:1883` |
| MQTT over TLS | `mqtts://broker.connectmq.com:8883` |
| WebSocket | `ws://broker.connectmq.com:8083/mqtt` |
| Secure WebSocket | `wss://broker.connectmq.com:8084/mqtt` |

**Swift (CocoaMQTT) — `MQTTExample.swift`** ([open file](public-broker/MQTTExample.swift))

```swift
import CocoaMQTT

let topic = "your-project/sensors/temperature" // Use a unique topic prefix: everyone can read the public broker

// Connect to the free public broker (no account needed) (Every client needs a unique client ID)
let mqtt = CocoaMQTT(clientID: "ios-" + UUID().uuidString, host: "broker.connectmq.com", port: 1883)
mqtt.keepAlive = 30

// Runs when the connection is established
mqtt.didConnectAck = { mqtt, _ in
    // Subscribe to the temperature topic
    mqtt.subscribe(topic, qos: .qos1)
    // Publish a JSON reading
    mqtt.publish(topic, withString: #"{"temperature":21.5}"#, qos: .qos1)
}
// Runs for every message on a subscribed topic
mqtt.didReceiveMessage = { _, message, _ in
    print(message.topic, message.string ?? "")
}
_ = mqtt.connect()
```

**Kotlin (HiveMQ MQTT Client) — `MqttExample.kt`** ([open file](public-broker/MqttExample.kt))

```kotlin
import com.hivemq.client.mqtt.MqttGlobalPublishFilter
import com.hivemq.client.mqtt.datatypes.MqttQos
import com.hivemq.client.mqtt.mqtt5.Mqtt5Client
import java.util.UUID

fun main() {
    val topic = "your-project/sensors/temperature" // Use a unique topic prefix: everyone can read the public broker

    // Connect to the free public broker (no account needed) (Every client needs a unique client ID)
    val client = Mqtt5Client.builder()
        .identifier("android-" + UUID.randomUUID())
        .serverHost("broker.connectmq.com")
        .serverPort(1883)
        .automaticReconnectWithDefaultConfig()
        .buildBlocking()
    client.connect()

    // Runs for every message on a subscribed topic
    client.toAsync().publishes(MqttGlobalPublishFilter.ALL) { p ->
        println("${p.topic}: ${String(p.payloadAsBytes)}")
    }
    // Subscribe to the temperature topic
    client.subscribeWith().topicFilter(topic).qos(MqttQos.AT_LEAST_ONCE).send()
    // Publish a JSON reading
    client.publishWith().topic(topic).qos(MqttQos.AT_LEAST_ONCE)
        .payload("""{"temperature":21.5}""".toByteArray()).send()
}
```

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic, including yours. Never send passwords, personal data or anything confidential through it, and use a unique topic prefix (`your-project/...`) so your messages don't mix with others'. There is no guarantee of availability or message retention. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=swift-kotlin-public)

## 2. Go to production with a private ConnectMQ broker

For real devices, use a private serverless MQTT broker on ConnectMQ instead of the public one: TLS encryption, a username and password for every device and per-topic access control, fully managed. The Serverless (Free) plan needs no credit card.

**Get your private broker in under a minute:**

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=swift-kotlin-private) — no credit card.
2. Create a broker in the dashboard (the **Serverless (Free)** plan is enough to start).
3. Copy the **host**, **username** and **password** of your broker.
4. Replace `YOUR_BROKER_HOST`, `YOUR_USERNAME` and `YOUR_PASSWORD` in the files under [`private-broker/`](private-broker/) and run them.

**Swift (CocoaMQTT) — `MQTTExample.swift`** ([open file](private-broker/MQTTExample.swift))

```swift
import CocoaMQTT

let topic = "your-project/sensors/temperature"

// Connect to your private ConnectMQ broker on port 8883 (Every client needs a unique client ID)
let mqtt = CocoaMQTT(clientID: "ios-" + UUID().uuidString, host: "YOUR_BROKER_HOST", port: 8883)
mqtt.keepAlive = 30
// Username and password from your ConnectMQ dashboard
mqtt.username = "YOUR_USERNAME"
mqtt.password = "YOUR_PASSWORD"
// TLS: the system CA store verifies the broker certificate
mqtt.enableSSL = true

// Runs when the connection is established
mqtt.didConnectAck = { mqtt, _ in
    // Subscribe to the temperature topic
    mqtt.subscribe(topic, qos: .qos1)
    // Publish a JSON reading
    mqtt.publish(topic, withString: #"{"temperature":21.5}"#, qos: .qos1)
}
// Runs for every message on a subscribed topic
mqtt.didReceiveMessage = { _, message, _ in
    print(message.topic, message.string ?? "")
}
_ = mqtt.connect()
```

**Kotlin (HiveMQ MQTT Client) — `MqttExample.kt`** ([open file](private-broker/MqttExample.kt))

```kotlin
import com.hivemq.client.mqtt.MqttGlobalPublishFilter
import com.hivemq.client.mqtt.datatypes.MqttQos
import com.hivemq.client.mqtt.mqtt5.Mqtt5Client
import java.util.UUID

fun main() {
    val topic = "your-project/sensors/temperature"

    // Connect to your private ConnectMQ broker on port 8883 (Every client needs a unique client ID)
    val client = Mqtt5Client.builder()
        .identifier("android-" + UUID.randomUUID())
        .serverHost("YOUR_BROKER_HOST")
        .serverPort(8883)
        // TLS: the system CA store verifies the broker certificate
        .sslWithDefaultConfig()
        // Username and password from your ConnectMQ dashboard
        .simpleAuth().username("YOUR_USERNAME").password("YOUR_PASSWORD".toByteArray()).applySimpleAuth()
        .automaticReconnectWithDefaultConfig()
        .buildBlocking()
    client.connect()

    // Runs for every message on a subscribed topic
    client.toAsync().publishes(MqttGlobalPublishFilter.ALL) { p ->
        println("${p.topic}: ${String(p.payloadAsBytes)}")
    }
    // Subscribe to the temperature topic
    client.subscribeWith().topicFilter(topic).qos(MqttQos.AT_LEAST_ONCE).send()
    // Publish a JSON reading
    client.publishWith().topic(topic).qos(MqttQos.AT_LEAST_ONCE)
        .payload("""{"temperature":21.5}""".toByteArray()).send()
}
```

### What you get with a private broker

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Devices & connections dashboard** — live device status, last values, connection history
- ⚡ **Fully managed and serverless** — no servers to patch or scale

<table>
  <tr>
    <td width="50%" valign="top"><a href="https://connectmq.com/monitoring/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=swift-kotlin-gallery"><img src="../assets/dashboard.png" alt="ConnectMQ dashboard: broker status, ISA-95 topic tree and live value cards with sparklines for every topic" width="100%"></a><br><b>Live dashboard</b> — broker status, ISA-95 topic tree and a live card for every topic</td>
    <td width="50%" valign="top"><a href="https://connectmq.com/digital-twin/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=swift-kotlin-gallery"><img src="../assets/digital-twin.png" alt="ConnectMQ 3D Digital Twin: machines bound to their MQTT topics with live telemetry" width="100%"></a><br><b>3D Digital Twin</b> — machines bound to their MQTT topics, telemetry on the equipment</td>
  </tr>
  <tr>
    <td width="50%" valign="top"><a href="https://connectmq.com/rules-alerts/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=swift-kotlin-gallery"><img src="../assets/rules.png" alt="ConnectMQ alert rules: conditions on JSON payload fields with message templates" width="100%"></a><br><b>Rules</b> — thresholds on JSON payload fields, such as <code>{temp} &gt; 70</code></td>
    <td width="50%" valign="top"><a href="https://connectmq.com/rules-alerts/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=swift-kotlin-gallery"><img src="../assets/alerts.png" alt="ConnectMQ triggered alerts: audit log with the exact payload that caused each alert" width="100%"></a><br><b>Alerts</b> — audit log with the exact payload, plus browser notifications</td>
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
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=swift-kotlin-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=swift-kotlin-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=swift-kotlin-footer">Pricing</a> ·
  <a href="https://connectmq.com/code-samples/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=swift-kotlin-footer">All code samples</a>
</p>
