# Build an MQTT Device Simulator in Python for Hundreds of Virtual Sensors

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-device-simulator-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-device-simulator-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

A complete Python MQTT device simulator that models hundreds of virtual sensors with drift, noise, faults and dropouts, schedules them under broker rate limits and publishes to broker.connectmq.com.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-device-simulator-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-device-simulator-intro)

📖 **Full step-by-step tutorial:** [Build an MQTT Device Simulator in Python for Hundreds of Virtual Sensors](https://connectmq.com/blog/mqtt-device-simulator/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-device-simulator-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-device-simulator-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`simulator.py`](simulator.py) | Simulates hundreds of virtual temperature/humidity sensors with a daily cycle, drift, noise, faults and dropouts, staggers them over the interval and rate-limits publishing to `connectmq/demo/<run-id>/<line>/<device>/telemetry` |
| [`requirements.txt`](requirements.txt) | Python dependency (`paho-mqtt>=2.0`) |

## Requirements

- Python 3 with `paho-mqtt` 2.x (everything else is the standard library)
- Optionally, `mosquitto_sub` to watch the stream

## Run it on the free public broker

1. Install the dependency:

   ```bash
   pip install "paho-mqtt>=2.0"
   ```

2. Run the simulator with the defaults (200 devices every 30 s, about 6.7 msg/s — under the public broker's 10 msg/s per client):

   ```bash
   python simulator.py --devices 200 --interval 30
   ```

3. The script prints the prefix it chose, for example `connectmq/demo/3f9a1c2e/#`. Watch the stream in a second terminal:

   ```bash
   mosquitto_sub -h broker.connectmq.com -p 1883 -i watch-3f9a1c2e -t "connectmq/demo/3f9a1c2e/#" -v
   ```

Other options: `--max-rate` (default 8 msg/s), `--fault-rate` (default 0.02), `--dropout` (default 0.01), `--prefix`, `--client-id`.

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-device-simulator-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-device-simulator-private) — the **Free** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. Pass your credentials, TLS and the issued client ID on the command line (use your broker host from the portal for `--host`):

   ```bash
   python simulator.py \
     --host broker.connectmq.com --port 8883 --tls \
     --username YOUR_USERNAME --password YOUR_PASSWORD --client-id YOUR_CLIENT_ID \
     --prefix connectmq/factory1/production \
     --devices 500 --interval 60 --max-rate 9
   ```

   Client IDs are bound to the issued credentials, so pass the ID from the portal rather than inventing one. To split a large fleet across several processes, give each process its own issued credentials.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [Build an MQTT Device Simulator in Python for Hundreds of Virtual Sensors](https://connectmq.com/blog/mqtt-device-simulator/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-device-simulator-related) — the full tutorial with explanations
- 🧩 [Python basic example](../../python/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-device-simulator-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-device-simulator-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-device-simulator-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-device-simulator-footer">Blog</a>
</p>
