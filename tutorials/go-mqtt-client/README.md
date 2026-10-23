# Go MQTT Client Tutorial with Eclipse Paho autopaho and MQTT 5

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-go-mqtt-client-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-go-mqtt-client-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Build a production-style Go MQTT client with paho.golang's autopaho package: MQTT 5 over TLS, automatic reconnects, resubscription, Last Will and graceful shutdown.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-go-mqtt-client-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-go-mqtt-client-intro)

📖 **Full step-by-step tutorial:** [Go MQTT Client Tutorial with Eclipse Paho autopaho and MQTT 5](https://connectmq.com/blog/go-mqtt-client/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-go-mqtt-client-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-go-mqtt-client-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`main.go`](main.go) | autopaho MQTT 5 client over TLS: env-based config, resubscribe in `OnConnectionUp`, Last Will + retained status, JSON telemetry every 5 s with message expiry, graceful shutdown. |

## Requirements

- Go 1.21 or newer
- `github.com/eclipse/paho.golang` (packages `autopaho` and `paho`)
- Optional: `mosquitto_sub` / `mosquitto_pub` to watch traffic and send commands

## Run it on the free public broker

1. Create the module and fetch the library (then copy `main.go` into the folder):

   ```bash
   mkdir go-mqtt-demo && cd go-mqtt-demo
   go mod init example.com/go-mqtt-demo
   go get github.com/eclipse/paho.golang@latest
   ```

2. Run it (defaults: `tls://broker.connectmq.com:8883`, prefix `connectmq/demo/x9p4tz`; override with `MQTT_CLIENT_ID` and `MQTT_PREFIX` to use your own random values):

   ```bash
   go run .
   ```

3. In a second terminal, watch the traffic and send a command:

   ```bash
   mosquitto_sub -h broker.connectmq.com -p 1883 -i watch-x9p4tz -t 'connectmq/demo/x9p4tz/#' -v
   mosquitto_pub -h broker.connectmq.com -p 1883 -i send-x9p4tz -t 'connectmq/demo/x9p4tz/cmd/led' -m 'on'
   ```

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-go-mqtt-client-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-go-mqtt-client-private) — the **Free** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. No code changes: `main.go` reads its settings from the environment. Use the exact client ID issued with your credentials:

   ```bash
   export MQTT_URL=tls://broker.connectmq.com:8883
   export MQTT_CLIENT_ID=YOUR_CLIENT_ID
   export MQTT_USERNAME=YOUR_USERNAME
   export MQTT_PASSWORD=YOUR_PASSWORD
   export MQTT_PREFIX=acme/site1/gateway1
   go run .
   ```

   In minimal container images (`scratch`, `distroless/static`) make sure CA certificates are present, otherwise the TLS handshake fails with `x509: certificate signed by unknown authority`.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [Go MQTT Client Tutorial with Eclipse Paho autopaho and MQTT 5](https://connectmq.com/blog/go-mqtt-client/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-go-mqtt-client-related) — the full tutorial with explanations
- 🧩 [Go basic example](../../go/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-go-mqtt-client-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-go-mqtt-client-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-go-mqtt-client-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-go-mqtt-client-footer">Blog</a>
</p>
