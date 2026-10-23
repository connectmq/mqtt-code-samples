# Log MQTT Messages to CSV with Python for Quick Analysis

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-log-mqtt-messages-to-csv-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-log-mqtt-messages-to-csv-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Build a Python logger that subscribes to MQTT topics, writes every message to CSV, rotates files by day and size, and produces data you can open straight in Excel, pandas or a notebook.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-log-mqtt-messages-to-csv-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-log-mqtt-messages-to-csv-intro)

📖 **Full step-by-step tutorial:** [Log MQTT Messages to CSV with Python for Quick Analysis](https://connectmq.com/blog/log-mqtt-messages-to-csv/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-log-mqtt-messages-to-csv-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-log-mqtt-messages-to-csv-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`mqtt_csv_logger.py`](mqtt_csv_logger.py) | Subscribes to MQTT topics and writes every message to CSV (long layout: `received_at`, `topic`, `qos`, `retain`, `value`, `payload`), rotating files daily and by size |
| [`analyze_csv.py`](analyze_csv.py) | Loads the logged CSV files with pandas, pivots numeric values per topic into 1-minute means and prints the message rate per topic |
| [`requirements.txt`](requirements.txt) | Python dependencies (`paho-mqtt>=2.0`, `pandas`) |

## Requirements

- Python 3.9 or newer
- `paho-mqtt` 2.x
- Optional: `mosquitto_pub` for sending test messages, and `pandas` for analysis

## Run it on the free public broker

1. Install the dependencies and start the logger (it subscribes to `connectmq/demo/csv-4821/#` by default; set `MQTT_TOPICS` to your own random prefix):

   ```bash
   pip install "paho-mqtt>=2.0" pandas
   python mqtt_csv_logger.py
   ```

2. In a second terminal, publish a few readings:

   ```bash
   for i in 1 2 3 4 5; do
     mosquitto_pub -h broker.connectmq.com -p 1883 -i pub-csv-4821 \
       -t connectmq/demo/csv-4821/line1/temp -m "{\"value\": 2$i.5, \"unit\": \"C\"}"
     mosquitto_pub -h broker.connectmq.com -p 1883 -i pub-csv-4821 \
       -t connectmq/demo/csv-4821/line1/status -m "running"
     sleep 1
   done
   ```

   You should see a file like `mqtt_logs/mqtt_2026-10-16_000.csv` with a header and ten rows.

3. Analyse the data:

   ```bash
   python analyze_csv.py
   ```

Other settings (environment variables): `CSV_DIR` (default `mqtt_logs`), `CSV_MAX_BYTES` (default 50 MB), `SKIP_RETAINED` (default `1`).

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-log-mqtt-messages-to-csv-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-log-mqtt-messages-to-csv-private) — the **Free** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. Run the same script with environment variables; TLS is enabled automatically when `MQTT_PORT` is `8883`. Use the client ID from the portal rather than a random one:

   ```bash
   export MQTT_HOST=YOUR_BROKER_HOST
   export MQTT_PORT=8883
   export MQTT_USERNAME=YOUR_USERNAME
   export MQTT_PASSWORD=YOUR_PASSWORD
   export MQTT_CLIENT_ID=YOUR_CLIENT_ID
   export MQTT_TOPICS="factory1/#"
   python mqtt_csv_logger.py
   ```

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [Log MQTT Messages to CSV with Python for Quick Analysis](https://connectmq.com/blog/log-mqtt-messages-to-csv/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-log-mqtt-messages-to-csv-related) — the full tutorial with explanations
- 🧩 [Python basic example](../../python/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-log-mqtt-messages-to-csv-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-log-mqtt-messages-to-csv-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-log-mqtt-messages-to-csv-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-log-mqtt-messages-to-csv-footer">Blog</a>
</p>
