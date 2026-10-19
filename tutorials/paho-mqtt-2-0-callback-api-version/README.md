# Paho MQTT 2.0 Callback API Version: Fixing Migration Errors Step by Step

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-2-0-callback-api-version-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-2-0-callback-api-version-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Paho-mqtt 2.0 broke a lot of Python code overnight. Learn what changed, how to fix the callback_api_version error in one line, and how to migrate every callback to the VERSION2 signatures with a working example.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-2-0-callback-api-version-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-2-0-callback-api-version-intro)

📖 **Full step-by-step tutorial:** [Paho MQTT 2.0 Callback API Version: Fixing Migration Errors Step by Step](https://connectmq.com/blog/paho-mqtt-2-0-callback-api-version/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-2-0-callback-api-version-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-2-0-callback-api-version-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`paho_v2_example.py`](paho_v2_example.py) | Complete VERSION2 example: `on_connect`, `on_subscribe`, `on_publish`, `on_message` and `on_disconnect` with the new signatures, publishing three QoS 1 messages over MQTT 5 |
| [`requirements.txt`](requirements.txt) | Python dependency (`paho-mqtt`, 2.x) |

## Requirements

- Python 3 (paho-mqtt 2.0 dropped Python 2.7 and very old Python 3 releases)
- [paho-mqtt](https://pypi.org/project/paho-mqtt/) 2.x

## Run it on the free public broker

1. Install paho-mqtt 2.x and run the example (change `k7f3q2` in `PREFIX` to your own random string first):

   ```bash
   pip install --upgrade paho-mqtt
   python paho_v2_example.py
   ```

   You should see the connect, the granted QoS, three publish acknowledgments and the three messages echoed back. Switch `protocol` to `mqtt.MQTTv311` and the same callbacks still work.

2. The one-line bridge if production is down (keeps the old 1.x callbacks, prints a deprecation warning):

   ```python
   import paho.mqtt.client as mqtt

   client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id="my-device")
   ```

3. Prove no VERSION1 client is left by turning warnings into errors:

   ```bash
   python -W error::DeprecationWarning paho_v2_example.py
   ```

Callback signatures after migrating:

| Callback | 1.x / VERSION1 signature | VERSION2 signature |
| --- | --- | --- |
| `on_connect` | `(client, userdata, flags, rc)` | `(client, userdata, flags, reason_code, properties)` |
| `on_disconnect` | `(client, userdata, rc)` | `(client, userdata, disconnect_flags, reason_code, properties)` |
| `on_subscribe` | `(client, userdata, mid, granted_qos)` | `(client, userdata, mid, reason_code_list, properties)` |
| `on_unsubscribe` | `(client, userdata, mid)` | `(client, userdata, mid, reason_code_list, properties)` |
| `on_publish` | `(client, userdata, mid)` | `(client, userdata, mid, reason_code, properties)` |
| `on_message` | `(client, userdata, message)` | unchanged |
| `on_log` | `(client, userdata, level, buf)` | unchanged |

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-2-0-callback-api-version-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-2-0-callback-api-version-private) — the **Serverless (Free)** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. In `paho_v2_example.py`, set `BROKER` to your broker host, use the generated client ID instead of the random one, add credentials and TLS before `connect()`, and connect on port 8883:

   ```python
   client.username_pw_set("YOUR_USERNAME", "YOUR_PASSWORD")
   client.tls_set()
   client.connect(BROKER, 8883, keepalive=60)
   ```

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [Paho MQTT 2.0 Callback API Version: Fixing Migration Errors Step by Step](https://connectmq.com/blog/paho-mqtt-2-0-callback-api-version/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-2-0-callback-api-version-related) — the full tutorial with explanations
- 🧩 [Python basic example](../../python/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-2-0-callback-api-version-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-2-0-callback-api-version-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-2-0-callback-api-version-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-2-0-callback-api-version-footer">Blog</a>
</p>
