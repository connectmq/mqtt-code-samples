# TIG Stack with Docker Compose for MQTT Data

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-tig-stack-docker-compose-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-tig-stack-docker-compose-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

A complete docker-compose setup for Telegraf, InfluxDB 2 and Grafana that subscribes to an MQTT broker, stores sensor data and opens with a provisioned data source and dashboard, plus the pitfalls that break first runs.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-tig-stack-docker-compose-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-tig-stack-docker-compose-intro)

📖 **Full step-by-step tutorial:** [TIG Stack with Docker Compose for MQTT Data](https://connectmq.com/blog/tig-stack-docker-compose/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-tig-stack-docker-compose-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-tig-stack-docker-compose-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`.env`](.env) | Placeholder secrets, InfluxDB names and MQTT connection settings read by Docker Compose (change them; keep your real one out of version control) |
| [`docker-compose.yml`](docker-compose.yml) | InfluxDB 2.7, Telegraf 1.32 and Grafana 11.3 with a health check and persistent volumes |
| [`telegraf/telegraf.conf`](telegraf/telegraf.conf) | `mqtt_consumer` input driven by environment variables, writing to InfluxDB |
| [`grafana/provisioning/datasources/influxdb.yml`](grafana/provisioning/datasources/influxdb.yml) | Provisions the InfluxDB (Flux) data source with a fixed `uid` |
| [`grafana/provisioning/dashboards/dashboards.yml`](grafana/provisioning/dashboards/dashboards.yml) | Tells Grafana where to load dashboard JSON files from |
| [`grafana/dashboards/mqtt-sensors.json`](grafana/dashboards/mqtt-sensors.json) | "MQTT Sensors" dashboard: temperature per device and a count of reporting devices |

## Requirements

- Docker with Docker Compose
- Mosquitto clients (`mosquitto_pub` / `mosquitto_sub`) or the [Python MQTT device simulator](https://connectmq.com/blog/mqtt-device-simulator/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-tig-stack-docker-compose-intro) as a data source
- Optional: `openssl` to generate a token

## Run it on the free public broker

1. Edit `.env`: replace `a1b2c3` with your own random string and set a real token (generate one with `openssl rand -hex 32`) and passwords.
2. Start the stack:

   ```bash
   cd tig-mqtt
   docker compose up -d
   docker compose ps
   docker compose logs -f telegraf
   ```

   (Here the stack folder is this directory.)

3. Publish data (or run the device simulator with `--prefix connectmq/demo/a1b2c3`):

   ```bash
   mosquitto_pub -h broker.connectmq.com -p 1883 -i pub-a1b2c3 \
     -t connectmq/demo/a1b2c3/line1/sensor-0001/telemetry \
     -m "{\"device\":\"sensor-0001\",\"ts\":$(date +%s%3N),\"temperature\":22.4,\"humidity\":41.0}"
   ```

4. Open http://localhost:3000, log in as `admin` with `GRAFANA_PASSWORD`, and open the **MQTT Sensors** dashboard in the **MQTT** folder.
5. Dashboard empty? Check each layer in order:

   ```bash
   mosquitto_sub -h broker.connectmq.com -p 1883 -i check-a1b2c3 -t "connectmq/demo/a1b2c3/#" -v
   docker compose logs telegraf
   docker compose exec influxdb influx query 'from(bucket: "sensors") |> range(start: -5m) |> limit(n: 3)'
   ```

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-tig-stack-docker-compose-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-tig-stack-docker-compose-private) — the **Free** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. Only `.env` changes. Set the MQTT values and run `docker compose up -d` again to recreate the Telegraf container:

   ```bash
   MQTT_SERVER=ssl://broker.connectmq.com:8883
   MQTT_TOPIC_PREFIX=connectmq/factory1/production
   MQTT_CLIENT_ID=YOUR_CLIENT_ID
   MQTT_USERNAME=YOUR_USERNAME
   MQTT_PASSWORD=YOUR_PASSWORD
   ```

   The certificate is issued by Let's Encrypt, so Telegraf trusts it without extra TLS settings. The `tags` pattern in `telegraf/telegraf.conf` assumes a three-level prefix; adjust the leading `_` segments if your prefix depth differs.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [TIG Stack with Docker Compose for MQTT Data](https://connectmq.com/blog/tig-stack-docker-compose/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-tig-stack-docker-compose-related) — the full tutorial with explanations
- 🧩 [Telegraf MQTT consumer tutorial](../telegraf-mqtt-consumer/) · [Telegraf json_v2 parser tutorial](../telegraf-json-v2-parser/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-tig-stack-docker-compose-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-tig-stack-docker-compose-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-tig-stack-docker-compose-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-tig-stack-docker-compose-footer">Blog</a>
</p>
