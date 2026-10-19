# Paho MQTT Python Tutorial: Publish and Subscribe in 10 Minutes

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-python-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-python-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Install paho-mqtt 2.x, build a working publisher and subscriber against broker.connectmq.com, learn the network loop, QoS, retained messages and Last Will, then switch to a private broker with credentials and TLS.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-python-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-python-intro)

📖 **Full step-by-step tutorial:** [Paho MQTT Python Tutorial: Publish and Subscribe in 10 Minutes](https://connectmq.com/blog/paho-mqtt-python/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-python-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-python-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`subscriber.py`](subscriber.py) | Subscriber that resubscribes in `on_connect`, reports granted QoS and prints every message (marking retained ones) using `loop_forever()` |
| [`publisher.py`](publisher.py) | Publisher with a retained Last Will, a retained `online` status and ten QoS 1 JSON readings using `loop_start()` |
| [`requirements.txt`](requirements.txt) | Python dependency (`paho-mqtt>=2.0`) |

## Requirements

- Python 3.8 or newer (`python --version`)
- [paho-mqtt](https://pypi.org/project/paho-mqtt/) 2.x
- Outbound access to port 1883, or 8883 for TLS
- Optional: `mosquitto_sub` to watch messages

## Run it on the free public broker

1. Create a virtual environment and install the library:

   ```bash
   python -m venv .venv
   source .venv/bin/activate          # Windows: .venv\Scripts\activate
   pip install "paho-mqtt>=2.0"
   python -c "import paho.mqtt; print(paho.mqtt.__version__)"
   ```

2. Change `k7f3q2` in both files to your own random string, then start the subscriber:

   ```bash
   python subscriber.py
   ```

   It prints "Connected" and "Subscribed with QoS 1", then waits.

3. In a second terminal, run the publisher:

   ```bash
   python publisher.py
   ```

   The subscriber prints the status message and ten sensor readings, one per second. Kill the publisher with `kill -9` instead of Ctrl+C and the broker sends the Last Will.

4. Verify from the other side with the Mosquitto client:

   ```bash
   mosquitto_sub -h broker.connectmq.com -p 1883 -i cli-k7f3q2 -t 'connectmq/demo/k7f3q2/#' -v
   ```

Public broker limits: 10 messages per second per client and 64 KB per message.

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-python-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-python-private) — the **Serverless (Free)** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. In `subscriber.py` and `publisher.py`, replace the client construction and `connect()` call with the post's private-broker version, using the host name shown for your broker in the portal:

   ```python
   client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="YOUR_CLIENT_ID")
   client.username_pw_set("YOUR_USERNAME", "YOUR_PASSWORD")
   client.tls_set()  # uses the system CA store and verifies the hostname
   client.connect("broker.connectmq.com", 8883, keepalive=60)
   ```

   Keep credentials in environment variables rather than in source files, and give each script its own client ID.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [Paho MQTT Python Tutorial: Publish and Subscribe in 10 Minutes](https://connectmq.com/blog/paho-mqtt-python/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-python-related) — the full tutorial with explanations
- 🧩 [Python basic example](../../python/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-python-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-python-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-python-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-python-footer">Blog</a>
</p>
