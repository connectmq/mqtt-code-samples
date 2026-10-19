# MQTT to Google Sheets: Send Sensor Data with Python and the Sheets API

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-google-sheets-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-google-sheets-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Use a Python MQTT subscriber, a Google service account and gspread to append batched sensor readings to a shared spreadsheet, without hitting API quotas or losing rows on reconnect.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-google-sheets-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-google-sheets-intro)

📖 **Full step-by-step tutorial:** [MQTT to Google Sheets: Send Sensor Data with Python and the Sheets API](https://connectmq.com/blog/mqtt-to-google-sheets/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-google-sheets-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-google-sheets-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`sheets_bridge.py`](sheets_bridge.py) | Subscribes to `<prefix>/<device>/<metric>`, queues readings and appends them to a Google Sheet in batches every 30 s with backoff on API errors |
| [`requirements.txt`](requirements.txt) | `paho-mqtt>=2.0` and `gspread>=6.0` |

## Requirements

- Python 3 with `paho-mqtt>=2.0` and `gspread>=6.0`
- A Google Cloud project with the **Google Sheets API** enabled and a service account JSON key saved as `service_account.json` next to the script
- A Google Sheet with a `Readings` tab (headers in row 1: `received_at`, `device`, `metric`, `value`, `topic`) shared with the service account email as an Editor
- Optional: `mosquitto_pub` to publish test readings

## Run it on the free public broker

1. Set up the service account and sheet as described above (sharing the sheet with the service account email is the step people forget).
2. Install the libraries:

   ```bash
   pip install "paho-mqtt>=2.0" "gspread>=6.0"
   ```

3. Run the bridge with the spreadsheet key (the long string between `/d/` and `/edit` in the sheet URL):

   ```bash
   export SHEET_KEY=your-spreadsheet-key
   python sheets_bridge.py
   ```

4. Publish some readings from another terminal:

   ```bash
   mosquitto_pub -h broker.connectmq.com -p 1883 -i gsheet-pub-5307 \
     -t connectmq/demo/gsheet-5307/boiler1/temperature -m '{"value": 64.2}'
   mosquitto_pub -h broker.connectmq.com -p 1883 -i gsheet-pub-5307 \
     -t connectmq/demo/gsheet-5307/boiler1/pressure -m 2.4
   ```

   Within 30 seconds both rows appear in the sheet. Use your own suffix instead of `gsheet-5307` (set `TOPIC_PREFIX`).

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-google-sheets-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-google-sheets-private) — the **Serverless (Free)** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. No code changes are needed: `sheets_bridge.py` reads the broker settings from the environment and enables TLS when the port is 8883:

   ```bash
   export MQTT_HOST=YOUR_BROKER_HOST
   export MQTT_PORT=8883
   export MQTT_USERNAME=YOUR_USERNAME
   export MQTT_PASSWORD=YOUR_PASSWORD
   export MQTT_CLIENT_ID=YOUR_CLIENT_ID
   ```

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [MQTT to Google Sheets: Send Sensor Data with Python and the Sheets API](https://connectmq.com/blog/mqtt-to-google-sheets/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-google-sheets-related) — the full tutorial with explanations
- 🧩 [Python basic example](../../python/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-google-sheets-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-google-sheets-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-google-sheets-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-google-sheets-footer">Blog</a>
</p>
