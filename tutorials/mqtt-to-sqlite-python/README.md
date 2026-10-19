# MQTT to SQLite with Python: Store and Query Sensor Messages

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-sqlite-python-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-sqlite-python-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Build a Python subscriber that stores every MQTT message in SQLite with a timestamp, topic, QoS and retain flag, using batched writes and WAL mode, then query history, hourly averages and latest values with plain SQL.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-sqlite-python-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-sqlite-python-intro)

📖 **Full step-by-step tutorial:** [MQTT to SQLite with Python: Store and Query Sensor Messages](https://connectmq.com/blog/mqtt-to-sqlite-python/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-sqlite-python-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-sqlite-python-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`mqtt_sqlite_logger.py`](mqtt_sqlite_logger.py) | paho-mqtt subscriber that queues messages and writes them to `mqtt_messages.db` in batched SQLite transactions (WAL mode) |
| [`requirements.txt`](requirements.txt) | Python dependency (`paho-mqtt>=2.0`) |

## Requirements

- Python 3 with a virtual environment (`sqlite3` ships with Python)
- [paho-mqtt](https://pypi.org/project/paho-mqtt/) 2.0 or newer
- Optional: `mosquitto_pub` / `mosquitto_sub` for test data, the `sqlite3` CLI or any SQLite browser for queries

## Run it on the free public broker

1. Create a virtual environment and install paho-mqtt:

   ```bash
   python -m venv .venv
   source .venv/bin/activate          # Windows: .venv\Scripts\activate
   pip install "paho-mqtt>=2.0"
   ```

2. Pick a random topic prefix (the code uses `connectmq/demo/k7f3q2`) and start the logger:

   ```bash
   python mqtt_sqlite_logger.py
   ```

3. In another terminal, publish some test data:

   ```bash
   for i in $(seq 1 20); do
     mosquitto_pub -h broker.connectmq.com -p 1883 -i sqlite-test-pub \
       -t "connectmq/demo/k7f3q2/sensors/room$((i % 2 + 1))" \
       -m "{\"temperature\": $((20 + RANDOM % 5)).$((RANDOM % 10)), \"humidity\": $((40 + RANDOM % 10))}"
     sleep 1
   done
   ```

   The logger prints "Stored 1 messages" about once a second. Stop it with Ctrl+C and the remaining queue is flushed before exit.

4. Query the history with `sqlite3 mqtt_messages.db`:

   ```sql
   SELECT received_at, payload
   FROM messages
   WHERE topic = 'connectmq/demo/k7f3q2/sensors/room1'
   ORDER BY received_at DESC
   LIMIT 10;
   ```

   Latest value per topic:

   ```sql
   SELECT topic, payload, MAX(received_at) AS last_seen
   FROM messages
   WHERE retained = 0
   GROUP BY topic;
   ```

   Hourly averages from JSON payloads:

   ```sql
   SELECT strftime('%Y-%m-%d %H:00', received_at)            AS hour,
          topic,
          ROUND(AVG(json_extract(payload, '$.temperature')), 2) AS avg_temperature,
          COUNT(*)                                             AS samples
   FROM messages
   WHERE topic LIKE 'connectmq/demo/k7f3q2/sensors/%'
     AND json_valid(payload)
   GROUP BY hour, topic
   ORDER BY hour;
   ```

   Keep only the last seven days and reclaim space:

   ```sql
   DELETE FROM messages
   WHERE received_at < strftime('%Y-%m-%dT%H:%M:%fZ', 'now', '-7 days');
   VACUUM;
   ```

5. If nothing is stored, check the topic filter with:

   ```bash
   mosquitto_sub -h broker.connectmq.com -p 1883 -i check-k7f3q2 -t 'connectmq/demo/k7f3q2/#' -v
   ```

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-sqlite-python-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-sqlite-python-private) — the **Serverless (Free)** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. In `mqtt_sqlite_logger.py`, set `BROKER` to your broker host and `PORT = 8883`, then uncomment the private-broker lines in `main()` that the post already includes:

   ```python
   # Private ConnectMQ broker:
   client.username_pw_set("YOUR_USERNAME", "YOUR_PASSWORD")
   client.tls_set()
   ```

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [MQTT to SQLite with Python: Store and Query Sensor Messages](https://connectmq.com/blog/mqtt-to-sqlite-python/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-sqlite-python-related) — the full tutorial with explanations
- 🧩 [Python basic example](../../python/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-sqlite-python-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-sqlite-python-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-sqlite-python-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-sqlite-python-footer">Blog</a>
</p>
