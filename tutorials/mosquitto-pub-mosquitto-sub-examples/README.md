# mosquitto_pub mosquitto_sub Examples: 25 Practical Commands for MQTT Testing

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mosquitto-pub-mosquitto-sub-examples-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mosquitto-pub-mosquitto-sub-examples-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

A copy-paste reference of 25 mosquitto_pub and mosquitto_sub commands covering QoS, retained messages, Last Will, TLS, output formatting and MQTT 5 properties, all runnable against broker.connectmq.com.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mosquitto-pub-mosquitto-sub-examples-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mosquitto-pub-mosquitto-sub-examples-intro)

📖 **Full step-by-step tutorial:** [mosquitto_pub mosquitto_sub Examples: 25 Practical Commands for MQTT Testing](https://connectmq.com/blog/mosquitto-pub-mosquitto-sub-examples/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mosquitto-pub-mosquitto-sub-examples-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mosquitto-pub-mosquitto-sub-examples-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`commands.sh`](commands.sh) | All 25 `mosquitto_pub` / `mosquitto_sub` / `mosquitto_rr` commands from the tutorial, grouped by topic (basics, QoS and sessions, retained messages, Last Will, scripting, TLS, MQTT 5). A reference sheet: run the commands one at a time |

## Requirements

- The Mosquitto clients (`mosquitto-clients` package), version 2.x for `-x`, `%j` output and some MQTT 5 options
- bash or zsh (the examples use shell variables)
- Optionally, `jq` for example 19

## Run it on the free public broker

1. Install the Mosquitto clients:

   ```bash
   # Debian / Ubuntu / Raspberry Pi OS
   sudo apt install mosquitto-clients

   # macOS
   brew install mosquitto

   # Windows: install Mosquitto from mosquitto.org; the installer includes mosquitto_pub.exe and mosquitto_sub.exe
   ```

2. Set two shell variables (replace `x7q2` with your own random string) and open two terminals, one for `mosquitto_sub` and one for `mosquitto_pub`:

   ```bash
   H="-h broker.connectmq.com -p 1883"
   T="connectmq/demo/x7q2"
   ```

3. Subscribe and publish:

   ```bash
   mosquitto_sub $H -i sub-x7q2 -t "$T/#" -v
   mosquitto_pub $H -i pub-x7q2 -t "$T/hello" -m "hello from the CLI"
   ```

4. Continue with any command from [`commands.sh`](commands.sh). Always pass a unique, non-empty client ID with `-i` — two clients with the same ID disconnect each other.

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mosquitto-pub-mosquitto-sub-examples-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mosquitto-pub-mosquitto-sub-examples-private) — the **Serverless (Free)** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. Every command works on your private broker by swapping the `-h ... -p 1883` flags for the TLS and credential flags of example 23:

   ```bash
   mosquitto_pub -h YOUR_BROKER_HOST -p 8883 --capath /etc/ssl/certs \
     -i YOUR_CLIENT_ID -u YOUR_USERNAME -P YOUR_PASSWORD \
     -t "factory1/line1/cnc1/telemetry" -q 1 -m '{"spindle_rpm": 8000}'
   ```

   On macOS or Windows, use `--cafile` with a PEM file containing the ISRG Root X1 certificate instead of `--capath`. To keep passwords out of shell history, put the `-u` and `-P` lines in `~/.config/mosquitto_pub` (and `mosquitto_sub`) with restrictive permissions.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [mosquitto_pub mosquitto_sub Examples: 25 Practical Commands for MQTT Testing](https://connectmq.com/blog/mosquitto-pub-mosquitto-sub-examples/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mosquitto-pub-mosquitto-sub-examples-related) — the full tutorial with explanations
- 🧩 [CLI basic example](../../cli/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mosquitto-pub-mosquitto-sub-examples-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mosquitto-pub-mosquitto-sub-examples-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mosquitto-pub-mosquitto-sub-examples-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mosquitto-pub-mosquitto-sub-examples-footer">Blog</a>
</p>
