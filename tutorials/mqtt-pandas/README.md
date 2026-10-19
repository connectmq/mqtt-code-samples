# Real-Time MQTT Data Analysis with Python and pandas

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-pandas-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-pandas-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Stream MQTT messages from a broker into pandas DataFrames without blocking the network loop, then compute rolling means, per-minute resamples, stale-device checks and simple anomaly flags.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-pandas-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-pandas-intro)

📖 **Full step-by-step tutorial:** [Real-Time MQTT Data Analysis with Python and pandas](https://connectmq.com/blog/mqtt-pandas/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-pandas-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-pandas-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`mqtt_pandas.py`](mqtt_pandas.py) | Buffers MQTT messages in a deque, drains them into pandas DataFrames every 10 s and prints rolling means, per-minute resamples, anomalies and stale devices |
| [`requirements.txt`](requirements.txt) | `paho-mqtt>=2.0` and `pandas>=2.1` |

## Requirements

- Python 3
- `paho-mqtt>=2.0` and `pandas>=2.1`
- A JSON telemetry stream, e.g. the simulator from the [MQTT device simulator tutorial](https://connectmq.com/blog/mqtt-device-simulator/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-pandas-intro), publishing to `connectmq/demo/<run-id>/<line>/<device>/telemetry`

## Run it on the free public broker

1. Install the dependencies:

   ```bash
   pip install "paho-mqtt>=2.0" "pandas>=2.1"
   ```

2. Start the device simulator and note the run ID it prints. Payloads look like this:

   ```json
   {"device": "sensor-0042", "ts": 1760600000123, "temperature": 21.84, "humidity": 44.2}
   ```

3. Set `RUN_ID` in `mqtt_pandas.py` to the simulator's run ID and run:

   ```bash
   python mqtt_pandas.py
   ```

   After ten seconds you see per-line averages, the five hottest devices and any anomalies or stale sensors. Press Ctrl+C to save the current window as `mqtt_snapshot.csv`.

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-pandas-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-pandas-private) — the **Serverless (Free)** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. Only the connection lines in `main()` of `mqtt_pandas.py` change:

   ```python
   client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="YOUR_CLIENT_ID")
   client.username_pw_set("YOUR_USERNAME", "YOUR_PASSWORD")
   client.tls_set()  # Let's Encrypt certificate, trusted by the system store
   client.connect("broker.connectmq.com", 8883, keepalive=30)
   ```

   Replace `broker.connectmq.com` with your broker's host (or set `BROKER` and `PORT = 8883`).

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [Real-Time MQTT Data Analysis with Python and pandas](https://connectmq.com/blog/mqtt-pandas/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-pandas-related) — the full tutorial with explanations
- 🧩 [Python basic example](../../python/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-pandas-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-pandas-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-pandas-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-pandas-footer">Blog</a>
</p>
