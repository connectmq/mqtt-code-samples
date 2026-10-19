# MQTT to TimescaleDB: Storing IoT Time Series in PostgreSQL

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-timescaledb-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-timescaledb-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Build an MQTT to TimescaleDB pipeline: a Python subscriber batches device messages into a PostgreSQL hypertable with COPY, then continuous aggregates, compression and retention keep queries fast and storage small.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-timescaledb-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-timescaledb-intro)

📖 **Full step-by-step tutorial:** [MQTT to TimescaleDB: Storing IoT Time Series in PostgreSQL](https://connectmq.com/blog/mqtt-to-timescaledb/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-timescaledb-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-timescaledb-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`mqtt_to_timescaledb.py`](mqtt_to_timescaledb.py) | MQTT 5 bridge: subscribes to `<prefix>/+/telemetry`, parses JSON into narrow rows and writes batches to TimescaleDB with `COPY` |
| [`schema.sql`](schema.sql) | Creates the `readings` hypertable (1-day chunks) and its device/metric/time index |
| [`continuous_aggregate.sql`](continuous_aggregate.sql) | One-minute continuous aggregate `readings_1m` plus its refresh policy |
| [`compression_retention.sql`](compression_retention.sql) | Compression (segment by device and metric) after 7 days and 90-day retention |
| [`requirements.txt`](requirements.txt) | Python dependencies (`paho-mqtt` 2.x, `psycopg[binary]` 3) |

## Requirements

- Docker (for the `timescale/timescaledb:latest-pg16` image) or another TimescaleDB on PostgreSQL 16
- `psql` client
- Python 3 with paho-mqtt 2.x and psycopg 3
- Optional: `mosquitto_pub` to simulate devices, Grafana for dashboards

## Run it on the free public broker

1. Start TimescaleDB:

   ```bash
   docker run -d --name tsdb -p 5432:5432 \
     -e POSTGRES_PASSWORD=change-me \
     -v tsdb-data:/var/lib/postgresql/data \
     timescale/timescaledb:latest-pg16
   ```

2. Create the schema (connect with `psql -h localhost -U postgres`), then optionally the aggregate and compression policies:

   ```bash
   psql -h localhost -U postgres -f schema.sql
   psql -h localhost -U postgres -f continuous_aggregate.sql
   psql -h localhost -U postgres -f compression_retention.sql
   ```

3. Install the dependencies:

   ```bash
   pip install "paho-mqtt>=2,<3" "psycopg[binary]>=3.1"
   ```

4. Start the bridge and publish test readings:

   ```bash
   python mqtt_to_timescaledb.py

   # in another terminal
   for i in $(seq 1 20); do
     mosquitto_pub -h broker.connectmq.com -p 1883 -i tsdb-sim-01 -q 1 \
       -t "connectmq/demo/tsdb-5b7e21/sensor-01/telemetry" \
       -m "{\"temperature\": 2$((RANDOM % 10)).$((RANDOM % 10)), \"humidity\": 4$((RANDOM % 10))}"
     sleep 1
   done
   ```

5. Check the data:

   ```sql
   SELECT device_id, metric, count(*), min(time), max(time)
   FROM readings GROUP BY device_id, metric;
   ```

   and query the one-minute aggregate:

   ```sql
   SELECT bucket, avg_value
   FROM readings_1m
   WHERE device_id = 'sensor-01' AND metric = 'temperature'
     AND bucket > now() - INTERVAL '24 hours'
   ORDER BY bucket;
   ```

   If the aggregate is empty, run `CALL refresh_continuous_aggregate('readings_1m', NULL, NULL);`. A Grafana panel query against the aggregate:

   ```sql
   SELECT bucket AS "time", device_id AS metric, avg_value
   FROM readings_1m
   WHERE $__timeFilter(bucket) AND metric = 'temperature'
   ORDER BY bucket;
   ```

The bridge is configured with environment variables: `MQTT_HOST` (default `broker.connectmq.com`), `MQTT_PORT` (default `8883`, TLS), `MQTT_USERNAME`, `MQTT_PASSWORD`, `MQTT_CLIENT_ID`, `MQTT_TOPIC_PREFIX` (default `connectmq/demo/tsdb-5b7e21`) and `PG_DSN`.

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-timescaledb-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-timescaledb-private) — the **Serverless (Free)** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. No code changes are needed: set the environment variables to the generated values and keep TLS on port 8883. Use a stable `MQTT_CLIENT_ID` so the persistent session survives restarts:

   ```bash
   export MQTT_HOST=YOUR_BROKER_HOST
   export MQTT_PORT=8883
   export MQTT_USERNAME=YOUR_USERNAME
   export MQTT_PASSWORD=YOUR_PASSWORD
   export MQTT_CLIENT_ID=YOUR_CLIENT_ID
   python mqtt_to_timescaledb.py
   ```

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [MQTT to TimescaleDB: Storing IoT Time Series in PostgreSQL](https://connectmq.com/blog/mqtt-to-timescaledb/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-timescaledb-related) — the full tutorial with explanations
- 🧩 [Python basic example](../../python/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-timescaledb-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-timescaledb-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-timescaledb-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-timescaledb-footer">Blog</a>
</p>
