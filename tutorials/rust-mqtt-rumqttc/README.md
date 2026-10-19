# Rust MQTT with rumqttc: Async Publish/Subscribe over TLS with Tokio

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-rust-mqtt-rumqttc-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-rust-mqtt-rumqttc-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Build an async Rust MQTT client with rumqttc and Tokio that connects over TLS with rustls, publishes JSON telemetry, receives commands and recovers from network errors.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-rust-mqtt-rumqttc-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-rust-mqtt-rumqttc-intro)

📖 **Full step-by-step tutorial:** [Rust MQTT with rumqttc: Async Publish/Subscribe over TLS with Tokio](https://connectmq.com/blog/rust-mqtt-rumqttc/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-rust-mqtt-rumqttc-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-rust-mqtt-rumqttc-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`Cargo.toml`](Cargo.toml) | Crate manifest with `rumqttc`, `tokio`, `serde` and `serde_json` |
| [`src/main.rs`](src/main.rs) | Async client: TLS via rustls on 8883, Last Will, JSON telemetry every 5 s, command subscription, retained `online` status and reconnects in the poll loop |

## Requirements

- Rust toolchain with Cargo (edition 2021)
- `rumqttc` 0.25 with the default `use-rustls` feature, and Tokio 1
- A C compiler and CMake on the build machine for the aws-lc-rs crypto provider (NASM may be needed on Windows)
- A system CA bundle on the runtime machine
- `mosquitto_sub` / `mosquitto_pub` for testing

## Run it on the free public broker

1. Build and run (the default prefix is `connectmq/demo/m3c8wd`; pick your own random one via `MQTT_PREFIX`):

   ```bash
   cargo run
   ```

2. In another terminal, watch and send a command:

   ```bash
   mosquitto_sub -h broker.connectmq.com -p 1883 -i watch-m3c8wd -t 'connectmq/demo/m3c8wd/#' -v
   mosquitto_pub -h broker.connectmq.com -p 1883 -i send-m3c8wd -t 'connectmq/demo/m3c8wd/cmd/fan' -m 'on'
   ```

   You should see telemetry every five seconds, a retained `online` on the status topic, and the command printed by the Rust program.

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-rust-mqtt-rumqttc-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-rust-mqtt-rumqttc-private) — the **Serverless (Free)** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. `src/main.rs` already uses TLS on 8883 and reads everything from the environment, so no code change is needed. Client IDs are bound to the credentials, so the ID must match exactly:

   ```bash
   export MQTT_HOST=broker.connectmq.com
   export MQTT_CLIENT_ID=YOUR_CLIENT_ID
   export MQTT_USERNAME=YOUR_USERNAME
   export MQTT_PASSWORD=YOUR_PASSWORD
   export MQTT_PREFIX=plant1/line2/edge-gateway
   cargo run --release
   ```

   Set `MQTT_HOST` to the host shown for your broker in the dashboard.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [Rust MQTT with rumqttc: Async Publish/Subscribe over TLS with Tokio](https://connectmq.com/blog/rust-mqtt-rumqttc/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-rust-mqtt-rumqttc-related) — the full tutorial with explanations
- 🧩 [Rust basic example](../../rust/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-rust-mqtt-rumqttc-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-rust-mqtt-rumqttc-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-rust-mqtt-rumqttc-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-rust-mqtt-rumqttc-footer">Blog</a>
</p>
