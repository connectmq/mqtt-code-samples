# Unity MQTT Client: Drive 3D Scenes with Live Sensor Data

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-unity-mqtt-client-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-unity-mqtt-client-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Add an MQTT client to Unity with MQTTnet, subscribe to sensor topics on broker.connectmq.com and safely animate GameObjects from live data on the main thread, the foundation of a digital twin.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-unity-mqtt-client-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-unity-mqtt-client-intro)

📖 **Full step-by-step tutorial:** [Unity MQTT Client: Drive 3D Scenes with Live Sensor Data](https://connectmq.com/blog/unity-mqtt-client/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-unity-mqtt-client-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-unity-mqtt-client-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`Assets/Scripts/MqttManager.cs`](Assets/Scripts/MqttManager.cs) | Singleton MQTTnet client: TLS connect, subscribe to a topic prefix, latest value per topic, reconnect with backoff, publish |
| [`Assets/Scripts/SpinFromTopic.cs`](Assets/Scripts/SpinFromTopic.cs) | Spins a transform at the RPM received on a topic, smoothed between messages |
| [`Assets/Scripts/ColorFromTemperature.cs`](Assets/Scripts/ColorFromTemperature.cs) | Colors a renderer along a gradient from a JSON temperature payload |
| [`Assets/link.xml`](Assets/link.xml) | Keeps IL2CPP code stripping from removing parts of MQTTnet |

Copy the `Assets/` contents into your Unity project's `Assets/` folder.

## Requirements

- Unity with Api Compatibility Level .NET Standard 2.1 (Project Settings > Player)
- MQTTnet 4.x (ships a .NET Standard build; newer major versions may not load in Unity), installed one of two ways:
  1. **NuGetForUnity**: NuGet > Manage NuGet Packages, search for MQTTnet and pick a 4.x version.
  2. **Manual**: download the `.nupkg` from nuget.org, rename it to `.zip`, extract `lib/netstandard2.1/MQTTnet.dll` into `Assets/Plugins/`.
- `link.xml` in `Assets/` when building with IL2CPP (iOS, often Android and consoles)
- Mosquitto clients (`mosquitto_pub`) to simulate sensors
- Not for WebGL: browsers do not allow raw TCP sockets (use MQTT over WebSocket via a `.jslib` bridge to `wss://broker.connectmq.com:8084/mqtt`)

## Run it on the free public broker

1. Install MQTTnet 4.x and copy the scripts into your project. Change `topicPrefix` (`connectmq/demo/u9n1ty`) to your own random string in the inspector.
2. Create an empty GameObject with `MqttManager`, a cylinder with `SpinFromTopic`, and a capsule with `ColorFromTemperature` (set a gradient on it).
3. Press Play, then simulate sensors from a terminal:

   ```bash
   # Spin the fan at 120 RPM, then 600 RPM
   mosquitto_pub -h broker.connectmq.com -p 1883 -i unity-sim-1 -t connectmq/demo/u9n1ty/fan1/rpm -m 120
   mosquitto_pub -h broker.connectmq.com -p 1883 -i unity-sim-1 -t connectmq/demo/u9n1ty/fan1/rpm -m 600

   # Heat the tank in a loop (bash)
   for t in $(seq 20 5 90); do
     mosquitto_pub -h broker.connectmq.com -p 1883 -i unity-sim-2 \
       -t connectmq/demo/u9n1ty/tank1/telemetry -m "{\"temperature\": $t}"
     sleep 0.5
   done
   ```

   The fan should ease up to speed and the tank should shift along your gradient.

4. To send commands from the scene, call for example `MqttManager.Instance.PublishAsync("pump1/cmd", "{\"action\":\"stop\"}")` from a UI button.

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-unity-mqtt-client-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-unity-mqtt-client-private) — the **Free** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. `MqttManager` already uses TLS on port 8883 (`useTls = true`). Select the `MqttManager` GameObject and fill these serialized fields in the inspector (or, better, load them at runtime from a config file outside the build):

   ```csharp
   [SerializeField] private string host = "YOUR_BROKER_HOST";
   [SerializeField] private int port = 8883;
   [SerializeField] private bool useTls = true;
   [SerializeField] private string topicPrefix = "YOUR_TOPIC_PREFIX";
   [SerializeField] private string username = "YOUR_USERNAME";
   [SerializeField] private string password = "YOUR_PASSWORD";
   ```

   Keep publish rights away from viewer apps where possible, so a decompiled build cannot inject fake sensor data.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [Unity MQTT Client: Drive 3D Scenes with Live Sensor Data](https://connectmq.com/blog/unity-mqtt-client/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-unity-mqtt-client-related) — the full tutorial with explanations
- 🧩 [C# basic example](../../csharp/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-unity-mqtt-client-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-unity-mqtt-client-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-unity-mqtt-client-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-unity-mqtt-client-footer">Blog</a>
</p>
