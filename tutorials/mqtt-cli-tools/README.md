# Best MQTT CLI Tools for Testing, Scripting and Debugging

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-cli-tools-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-cli-tools-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

A hands-on comparison of mosquitto_pub/sub, MQTTX CLI, HiveMQ MQTT CLI, the MQTT.js CLI, curl and mqttui, with the same test run against broker.connectmq.com so you can choose the right tool for scripting and debugging.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-cli-tools-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-cli-tools-intro)

📖 **Full step-by-step tutorial:** [Best MQTT CLI Tools for Testing, Scripting and Debugging](https://connectmq.com/blog/mqtt-cli-tools/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-cli-tools-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-cli-tools-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`commands.sh`](commands.sh) | The commands from the comparison for mosquitto_pub/sub, MQTTX CLI, HiveMQ MQTT CLI, the MQTT.js CLI, curl and mqttui, plus the "same test in every tool" one-liners and the private-broker command. A reference sheet: run the commands one at a time |

## Requirements

Install whichever tools you want to try:

- **mosquitto_pub / mosquitto_sub** — OS package `mosquitto-clients`
- **MQTTX CLI** — npm, Homebrew or binary
- **HiveMQ MQTT CLI** — Homebrew, package or JAR (some installs need a Java runtime)
- **MQTT.js CLI** — `npm install -g mqtt` (Node.js)
- **curl** — usually preinstalled; check `curl -V` for `mqtt` in the protocol list (MQTT 3.1.1, QoS 0 only)
- **mqttui** — Cargo or binary

Note: both the HiveMQ CLI and the MQTT.js CLI install a command called `mqtt`; whichever comes first on your `PATH` wins.

## Run it on the free public broker

1. Start a subscriber with any tool, for example:

   ```bash
   mosquitto_sub -h broker.connectmq.com -p 1883 -i cli-cmp-sub1 -t 'connectmq/demo/c1t9/#' -v
   ```

2. Publish from another terminal (with the same or a different tool):

   ```bash
   mosquitto_pub -h broker.connectmq.com -p 1883 -i cli-cmp-pub1 -t connectmq/demo/c1t9/test -m 'hello' -q 1
   ```

3. Try the equivalent commands for the other tools in [`commands.sh`](commands.sh). Always set a unique client ID per terminal and use your own topic prefix instead of `connectmq/demo/c1t9/`.

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-cli-tools-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-cli-tools-private) — the **Free** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. Every tool takes the same three things: host and TLS port 8883, credentials and the exact client ID from the portal (a random ID will be rejected). For example:

   ```bash
   mosquitto_sub -h YOUR_BROKER_HOST -p 8883 --capath /etc/ssl/certs \
     -i YOUR_CLIENT_ID -u YOUR_USERNAME -P YOUR_PASSWORD -t '#' -v
   ```

   For the other tools: MQTTX CLI uses `-l mqtts`, HiveMQ CLI uses `-s`, and curl uses `mqtts://`. curl generates its own client ID, so it cannot be used against a broker that requires a specific client ID per credential. Tools that support WebSocket can use port 8083 or secure WebSocket on 8084 at path `/mqtt`.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [Best MQTT CLI Tools for Testing, Scripting and Debugging](https://connectmq.com/blog/mqtt-cli-tools/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-cli-tools-related) — the full tutorial with explanations
- 🧩 [CLI basic example](../../cli/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-cli-tools-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-cli-tools-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-cli-tools-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-cli-tools-footer">Blog</a>
</p>
