# Android MQTT Kotlin Client: Connect, Subscribe and Notify

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-android-mqtt-kotlin-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-android-mqtt-kotlin-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Build an Android app in Kotlin that connects to an MQTT broker over TLS, subscribes to alarm topics, raises system notifications and reconnects correctly as the app moves between foreground and background.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-android-mqtt-kotlin-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-android-mqtt-kotlin-intro)

📖 **Full step-by-step tutorial:** [Android MQTT Kotlin Client: Connect, Subscribe and Notify](https://connectmq.com/blog/android-mqtt-kotlin/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-android-mqtt-kotlin-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-android-mqtt-kotlin-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`MqttRepository.kt`](MqttRepository.kt) | Single app-wide HiveMQ MQTT 5 client over TLS: auto-reconnect, alarm subscription, `StateFlow` state and notifications. |
| [`AlarmApp.kt`](AlarmApp.kt) | `Application` class that connects/disconnects with the app's foreground lifecycle via `ProcessLifecycleOwner`. |
| [`MainActivity.kt`](MainActivity.kt) | Compose activity that requests notification permission and shows connection state and the last alarm. |

## Requirements

- Android Studio, a project created from the Empty Activity (Compose) template, package `com.example.mqttalarms`
- `minSdk` 26 or higher
- HiveMQ MQTT Client `com.hivemq:hivemq-mqtt-client:1.3.3` and `androidx.lifecycle:lifecycle-process:2.8.7`
- Optional: `mosquitto_pub` to simulate a device

## Run it on the free public broker

1. Add the dependencies and the Netty packaging excludes to `app/build.gradle.kts`:

   ```kotlin
   android {
       defaultConfig {
           minSdk = 26
       }
       packaging {
           resources {
               // Netty, used internally by the client, ships duplicate metadata files
               excludes += setOf("META-INF/INDEX.LIST", "META-INF/io.netty.versions.properties")
           }
       }
   }

   dependencies {
       implementation("com.hivemq:hivemq-mqtt-client:1.3.3") // check Maven Central for the latest 1.3.x
       implementation("androidx.lifecycle:lifecycle-process:2.8.7")
   }
   ```

2. Add the permissions to `AndroidManifest.xml` and register the application class with `android:name=".AlarmApp"` on the `<application>` element:

   ```xml
   <uses-permission android:name="android.permission.INTERNET" />
   <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
   ```

3. Copy `MqttRepository.kt`, `AlarmApp.kt` and `MainActivity.kt` into the `com.example.mqttalarms` package. Change `PREFIX` in `MqttRepository.kt` to your own topic prefix.
4. Run the app, allow notifications, then publish an alarm as a device would:

   ```bash
   mosquitto_pub -h broker.connectmq.com -p 1883 -i android-test-a7k2 \
     -t connectmq/demo/a7k2/pump3/alarm -q 1 -m "Pressure above 8 bar"
   ```

   A heads-up notification appears. Toggle airplane mode to watch the status flip to "Disconnected" and back.

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-android-mqtt-kotlin-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-android-mqtt-kotlin-private) — the **Free** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. In `MqttRepository.kt`, swap the builder lines of the `client` property (the client ID must be the one issued with your credentials):

   ```kotlin
   MqttClient.builder()
       .useMqttVersion5()
       .identifier("YOUR_CLIENT_ID")
       .serverHost("YOUR_BROKER_HOST")
       .serverPort(8883)
       .sslWithDefaultConfig()
       .simpleAuth()
           .username("YOUR_USERNAME")
           .password("YOUR_PASSWORD".toByteArray())
           .applySimpleAuth()
       // ... reconnect and listeners as before
       .buildAsync()
   ```

   Do not hard-code a shared credential into a published APK; provision per-install credentials from your backend and store them with the Android Keystore.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [Android MQTT Kotlin Client: Connect, Subscribe and Notify](https://connectmq.com/blog/android-mqtt-kotlin/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-android-mqtt-kotlin-related) — the full tutorial with explanations
- 🧩 [Swift and Kotlin basic examples](../../swift-kotlin/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-android-mqtt-kotlin-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-android-mqtt-kotlin-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-android-mqtt-kotlin-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-android-mqtt-kotlin-footer">Blog</a>
</p>
