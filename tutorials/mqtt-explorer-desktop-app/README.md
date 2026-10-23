# MQTT Explorer Desktop App Comparison: Visualizing Topic Trees

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-explorer-desktop-app-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-explorer-desktop-app-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Compare desktop MQTT explorers, including MQTT Explorer, MQTTX, MQTT.fx and the ConnectMQ Desktop MQTT explorer, learn what features matter when debugging topic trees, and connect any of them to broker.connectmq.com.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-explorer-desktop-app-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-explorer-desktop-app-intro)

📖 **Full step-by-step tutorial:** [MQTT Explorer Desktop App Comparison: Visualizing Topic Trees](https://connectmq.com/blog/mqtt-explorer-desktop-app/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-explorer-desktop-app-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-explorer-desktop-app-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`commands.sh`](commands.sh) | Seeds a small retained ISA-95 style topic tree (`plant1/line1/cnc1/...`) under your prefix and publishes a live tank level for 60 seconds, so you can compare explorers on the same data |

## Requirements

- An MQTT desktop explorer: MQTT Explorer, MQTTX, MQTT.fx or the ConnectMQ Desktop MQTT explorer
- The Mosquitto clients (`mosquitto_pub`) and bash to seed the topic tree

## Run it on the free public broker

1. Replace `ex4m` in `commands.sh` with your own random string and run it:

   ```bash
   bash commands.sh
   ```

2. Connect your explorer with these settings:

   | Field | Public broker (testing) |
   | --- | --- |
   | Host | `broker.connectmq.com` |
   | Port / protocol | 1883 TCP, or 8883 with TLS on |
   | WebSocket | 8083 (`ws`), 8084 (`wss`), path `/mqtt` |
   | Client ID | Any unique, non-empty value |
   | Username / password | Empty |
   | Subscription | `connectmq/demo/ex4m/#` |

3. Explore: expand `plant1` and check the hierarchy, watch `tank1/level` history while the loop runs, check that `furnace1/telemetry` JSON is pretty-printed, delete the retained `cnc1/status` by publishing an empty retained payload, then disconnect and reconnect to see which topics are retained.

Avoid the default `#` subscription of some explorers on the public broker: subscribe only to your own prefix.

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-explorer-desktop-app-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-explorer-desktop-app-private) — the **Free** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. In your explorer's connection settings, use:

   | Field | Your private broker |
   | --- | --- |
   | Host | Your broker host from the portal |
   | Port / protocol | 8883 with TLS (recommended) |
   | WebSocket | 8083 (`ws`), 8084 (`wss`), path `/mqtt` |
   | Client ID | The client ID generated for your credentials |
   | Username / password | `YOUR_USERNAME` / `YOUR_PASSWORD` |
   | Subscription | `#` or your own root |

   If TLS fails, add the ISRG Root X1 certificate (Let's Encrypt) as the CA in apps that do not use the system trust store, and check your system clock.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [MQTT Explorer Desktop App Comparison: Visualizing Topic Trees](https://connectmq.com/blog/mqtt-explorer-desktop-app/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-explorer-desktop-app-related) — the full tutorial with explanations
- 🧩 [CLI basic example](../../cli/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-explorer-desktop-app-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-explorer-desktop-app-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-explorer-desktop-app-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-explorer-desktop-app-footer">Blog</a>
</p>
