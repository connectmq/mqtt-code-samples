# Qt MQTT Client in C++: Building Desktop and Embedded HMIs

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-qt-mqtt-client-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-qt-mqtt-client-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Use the Qt MQTT module to build a C++ HMI that connects to a cloud broker over TLS, subscribes to machine topics, shows live values with staleness detection and sends operator commands.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-qt-mqtt-client-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-qt-mqtt-client-intro)

📖 **Full step-by-step tutorial:** [Qt MQTT Client in C++: Building Desktop and Embedded HMIs](https://connectmq.com/blog/qt-mqtt-client/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-qt-mqtt-client-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-qt-mqtt-client-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`CMakeLists.txt`](CMakeLists.txt) | CMake project that builds `press_hmi` against Qt6 Widgets, Network and Mqtt |
| [`main.cpp`](main.cpp) | `PressPanel` HMI: TLS connection on 8883, subscribe on connect, reconnect with exponential backoff, stale-value greying and START/STOP commands at QoS 1 |

Topics used by the HMI (`<prefix>` defaults to `connectmq/demo/qt-hmi-3f81`):

| Tag | Topic | Payload |
|---|---|---|
| Oil temperature | `<prefix>/line1/press1/temperature` | `48.2` |
| Pressure | `<prefix>/line1/press1/pressure` | `182.5` |
| State | `<prefix>/line1/press1/state` | `RUNNING`, `IDLE`, `FAULT` |
| Command | `<prefix>/line1/press1/cmd` | `START` or `STOP` |

## Requirements

- Qt 6 with the **Qt MQTT** add-on module (Maintenance Tool → Additional Libraries → Qt MQTT, a `qtmqtt` distro/Yocto package, or built from source). Qt MQTT is licensed under GPLv3 or a commercial Qt licence.
- CMake 3.21+ and a C++17 compiler
- Qt's OpenSSL/TLS backend and a system CA bundle
- `mosquitto_pub` / `mosquitto_sub` to simulate the machine

## Run it on the free public broker

1. Build and run the HMI (adjust the Qt path to your installation):

   ```bash
   cmake -B build -DCMAKE_PREFIX_PATH=$HOME/Qt/6.8.0/gcc_64
   cmake --build build
   ./build/press_hmi
   ```

2. Simulate the press from a terminal (synthetic values only — the public area is readable by everyone):

   ```bash
   P="connectmq/demo/qt-hmi-3f81/line1/press1"

   mosquitto_pub -h broker.connectmq.com -p 1883 -i qt-sim-state -r -t "$P/state" -m "RUNNING"

   while true; do
     mosquitto_pub -h broker.connectmq.com -p 1883 -i qt-sim-temp -t "$P/temperature" -m "4$((RANDOM % 10)).$((RANDOM % 10))"
     mosquitto_pub -h broker.connectmq.com -p 1883 -i qt-sim-pres -t "$P/pressure" -m "18$((RANDOM % 10)).0"
     sleep 1
   done
   ```

3. In a third terminal, watch the commands the HMI sends when you press START / STOP:

   ```bash
   mosquitto_sub -h broker.connectmq.com -p 1883 -i qt-sim-cmd -t "$P/cmd" -v
   ```

   Stop the loop and the temperature and pressure values turn grey after 10 seconds.

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-qt-mqtt-client-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-qt-mqtt-client-private) — the **Serverless (Free)** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. `main.cpp` already connects with TLS on port 8883 and reads credentials from the environment. Change `m_client.setHostname("broker.connectmq.com")` in `setupClient()` to your broker host, then set the panel's environment (for example in its systemd unit):

   ```bash
   MQTT_USERNAME=YOUR_USERNAME
   MQTT_PASSWORD=YOUR_PASSWORD
   MQTT_CLIENT_ID=YOUR_CLIENT_ID
   MQTT_TOPIC_PREFIX=YOUR_TOPIC_PREFIX
   ```

   Give every panel its own credentials — ConnectMQ binds client IDs to issued credentials, and two panels with the same client ID keep kicking each other off.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [Qt MQTT Client in C++: Building Desktop and Embedded HMIs](https://connectmq.com/blog/qt-mqtt-client/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-qt-mqtt-client-related) — the full tutorial with explanations
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-qt-mqtt-client-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-qt-mqtt-client-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-qt-mqtt-client-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-qt-mqtt-client-footer">Blog</a>
</p>
