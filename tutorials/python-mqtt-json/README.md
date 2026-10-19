# Python MQTT JSON: Publishing Sensor Data with Timestamps and Schema Versions

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-python-mqtt-json-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-python-mqtt-json-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Turn Python sensor readings into clean JSON MQTT messages: compact encoding, UTC timestamps, sequence numbers, schema versioning, NaN-safe serialization and MQTT 5 content type, plus a validating subscriber.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-python-mqtt-json-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-python-mqtt-json-intro)

📖 **Full step-by-step tutorial:** [Python MQTT JSON: Publishing Sensor Data with Timestamps and Schema Versions](https://connectmq.com/blog/python-mqtt-json/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-python-mqtt-json-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-python-mqtt-json-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`json_publisher.py`](json_publisher.py) | Publishes simulated sensor readings as compact, NaN-safe JSON with UTC timestamps, sequence numbers, a schema version and MQTT 5 content type |
| [`json_subscriber.py`](json_subscriber.py) | Subscribes to `sensors/+/telemetry`, validates JSON, required fields and schema version, and rejects bad messages without crashing |
| [`requirements.txt`](requirements.txt) | Python dependency (`paho-mqtt>=2.0`) |

Payload format used by both scripts:

```json
{
  "v": 1,
  "device": "room1",
  "ts": "2026-10-16T08:15:30.123Z",
  "seq": 42,
  "temperature_c": 21.4,
  "humidity_pct": 45.2,
  "battery_v": null
}
```

## Requirements

- Python 3
- [paho-mqtt](https://pypi.org/project/paho-mqtt/) 2.0 or newer
- Optional: `mosquitto_sub` and `jq` to inspect messages

## Run it on the free public broker

Change `k7f3q2` in `PREFIX` to your own random string so you stay separate from other users of the public broker.

1. Install paho-mqtt:

   ```bash
   pip install "paho-mqtt>=2.0"
   ```

2. Start the publisher. Every two seconds it prints a payload; about one in twenty readings shows `null` values where the simulated sensor failed:

   ```bash
   python json_publisher.py
   ```

   ```text
    116 bytes  {"device":"room1","ts":"2026-10-16T08:15:30.123Z","seq":42,"temperature_c":21.4,"humidity_pct":45.2,"battery_v":null,"v":1}
   ```

3. In another terminal, start the validating subscriber:

   ```bash
   python json_subscriber.py
   ```

4. Or inspect the raw JSON with `mosquitto_sub` and `jq`:

   ```bash
   mosquitto_sub -h broker.connectmq.com -p 1883 -i json-inspect-k7f3q2 -t 'connectmq/demo/k7f3q2/sensors/+/telemetry' | jq .
   ```

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-python-mqtt-json-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-python-mqtt-json-private) — the **Serverless (Free)** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. In `json_publisher.py`, set `BROKER` to your broker host and `PORT = 8883`, then add the lines from the post's comment before `client.connect(...)`:

   ```python
   # Private ConnectMQ broker: client.username_pw_set("YOUR_USERNAME", "YOUR_PASSWORD"); client.tls_set(); port 8883
   client.username_pw_set("YOUR_USERNAME", "YOUR_PASSWORD")
   client.tls_set()
   ```

   Do the same in `json_subscriber.py` (`client.username_pw_set(...)`, `client.tls_set()`, and `client.connect("YOUR_BROKER_HOST", 8883, keepalive=60)`). Use a separate username and password for each script.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [Python MQTT JSON: Publishing Sensor Data with Timestamps and Schema Versions](https://connectmq.com/blog/python-mqtt-json/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-python-mqtt-json-related) — the full tutorial with explanations
- 🧩 [Python basic example](../../python/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-python-mqtt-json-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-python-mqtt-json-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-python-mqtt-json-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-python-mqtt-json-footer">Blog</a>
</p>
