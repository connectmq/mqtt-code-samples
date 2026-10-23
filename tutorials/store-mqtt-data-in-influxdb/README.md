# How to Store MQTT Data in InfluxDB with Python

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-store-mqtt-data-in-influxdb-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-store-mqtt-data-in-influxdb-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Build a Python bridge with paho-mqtt and influxdb-client that subscribes to a broker, turns topic levels into InfluxDB tags, writes numeric JSON values as fields in batches and handles bad payloads and type conflicts.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-store-mqtt-data-in-influxdb-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-store-mqtt-data-in-influxdb-intro)

📖 **Full step-by-step tutorial:** [How to Store MQTT Data in InfluxDB with Python](https://connectmq.com/blog/store-mqtt-data-in-influxdb/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-store-mqtt-data-in-influxdb-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-store-mqtt-data-in-influxdb-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`mqtt_influx_bridge.py`](mqtt_influx_bridge.py) | MQTT-to-InfluxDB bridge: maps topic levels to tags via `TOPIC_SCHEMA`, writes JSON numbers as float fields in batches, skips bad payloads and logs `written`/`skipped` counters |
| [`requirements.txt`](requirements.txt) | Python dependencies (`paho-mqtt>=2.0`, `influxdb-client`) |

Data model — a topic and payload like

```text
connectmq/demo/a1b2c3/line1/sensor-0042/telemetry
```

```json
{"device": "sensor-0042", "ts": 1760600000123, "temperature": 21.84, "humidity": 44.2}
```

become this InfluxDB point:

```text
telemetry,line=line1,device=sensor-0042 temperature=21.84,humidity=44.2 1760600000123000000
```

## Requirements

- Python 3 with [paho-mqtt](https://pypi.org/project/paho-mqtt/) 2.0+ and [influxdb-client](https://influxdb-client.readthedocs.io/en/stable/) (InfluxDB 2.x client)
- InfluxDB 2 (e.g. in Docker) with an org, a bucket and a token with write access
- A data source publishing JSON telemetry, e.g. the [MQTT device simulator](../mqtt-device-simulator/)
- Optional: the `influx` CLI to query the data

## Run it on the free public broker

1. Start InfluxDB 2 in Docker (the init variables create the `iot` org, the `sensors` bucket and an admin token):

   ```bash
   docker run -d --name influxdb -p 8086:8086 \
     -v influxdb-data:/var/lib/influxdb2 \
     -e DOCKER_INFLUXDB_INIT_MODE=setup \
     -e DOCKER_INFLUXDB_INIT_USERNAME=admin \
     -e DOCKER_INFLUXDB_INIT_PASSWORD=change-me-please \
     -e DOCKER_INFLUXDB_INIT_ORG=iot \
     -e DOCKER_INFLUXDB_INIT_BUCKET=sensors \
     -e DOCKER_INFLUXDB_INIT_RETENTION=30d \
     -e DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=my-super-secret-token \
     influxdb:2.7
   ```

2. Install the Python packages:

   ```bash
   pip install "paho-mqtt>=2.0" influxdb-client
   ```

3. Run the bridge, with `MQTT_TOPIC` set to your data source's prefix:

   ```bash
   export INFLUX_TOKEN=my-super-secret-token
   export MQTT_TOPIC="connectmq/demo/3f9a1c2e/+/+/telemetry"
   python mqtt_influx_bridge.py
   ```

4. Check the data in the InfluxDB Data Explorer or with the CLI:

   ```bash
   influx query 'from(bucket: "sensors")
     |> range(start: -10m)
     |> filter(fn: (r) => r._measurement == "telemetry" and r._field == "temperature")
     |> group(columns: ["line"])
     |> mean()' --org iot --token my-super-secret-token
   ```

A different topic layout only needs a new schema, e.g. `TOPIC_SCHEMA="_/site/area/line/device/@measurement"` for `connectmq/factory1/production/line1/cnc1/telemetry`.

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-store-mqtt-data-in-influxdb-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-store-mqtt-data-in-influxdb-private) — the **Free** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. The bridge itself does not change — everything is configured through environment variables. Enable TLS on port 8883 and use the credentials and fixed client ID from the portal:

   ```bash
   export MQTT_HOST=YOUR_BROKER_HOST
   export MQTT_PORT=8883
   export MQTT_TLS=1
   export MQTT_USERNAME=YOUR_USERNAME
   export MQTT_PASSWORD=YOUR_PASSWORD
   export MQTT_CLIENT_ID=YOUR_CLIENT_ID
   export MQTT_TOPIC="YOUR_TOPIC_PREFIX/+/+/telemetry"
   export INFLUX_TOKEN=YOUR_INFLUX_WRITE_TOKEN
   python mqtt_influx_bridge.py
   ```

   Use a dedicated InfluxDB token scoped to one bucket instead of the admin token.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [How to Store MQTT Data in InfluxDB with Python](https://connectmq.com/blog/store-mqtt-data-in-influxdb/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-store-mqtt-data-in-influxdb-related) — the full tutorial with explanations
- 🧩 [Python basic example](../../python/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-store-mqtt-data-in-influxdb-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-store-mqtt-data-in-influxdb-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-store-mqtt-data-in-influxdb-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-store-mqtt-data-in-influxdb-footer">Blog</a>
</p>
