# Telegraf MQTT Consumer: Ingest MQTT Data into InfluxDB

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-telegraf-mqtt-consumer-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-telegraf-mqtt-consumer-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

A practical guide to Telegraf's mqtt_consumer input: subscribe to broker topics, parse JSON with timestamps and tags, write to InfluxDB 2, secure the connection with TLS and troubleshoot missing data.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-telegraf-mqtt-consumer-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-telegraf-mqtt-consumer-intro)

📖 **Full step-by-step tutorial:** [Telegraf MQTT Consumer: Ingest MQTT Data into InfluxDB](https://connectmq.com/blog/telegraf-mqtt-consumer/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-telegraf-mqtt-consumer-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-telegraf-mqtt-consumer-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`telegraf.conf`](telegraf.conf) | Telegraf config: `mqtt_consumer` subscribing to JSON telemetry, topic parsing for a `line` tag, output to InfluxDB 2 and stdout |

## Requirements

- Telegraf 1.30 or newer (native package or the `telegraf` Docker image)
- InfluxDB 2.7 with an org, bucket and API token
- Mosquitto clients (`mosquitto_pub` / `mosquitto_sub`) for test messages

## Run it on the free public broker

1. If you do not have InfluxDB yet, start it with Docker:

   ```bash
   docker run -d --name influxdb -p 8086:8086 \
     -e DOCKER_INFLUXDB_INIT_MODE=setup \
     -e DOCKER_INFLUXDB_INIT_USERNAME=admin \
     -e DOCKER_INFLUXDB_INIT_PASSWORD=change-me-please \
     -e DOCKER_INFLUXDB_INIT_ORG=iot \
     -e DOCKER_INFLUXDB_INIT_BUCKET=sensors \
     -e DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=my-super-secret-token \
     influxdb:2.7
   ```

2. Replace `a1b2c3` in `telegraf.conf` with your own random run ID.
3. Set the token and run Telegraf in test mode:

   ```bash
   export INFLUX_TOKEN=my-super-secret-token
   telegraf --config telegraf.conf --test --test-wait 20
   ```

4. While that runs, publish a test message from another terminal:

   ```bash
   mosquitto_pub -h broker.connectmq.com -p 1883 -i pub-a1b2c3 \
     -t connectmq/demo/a1b2c3/line1/sensor-0001/telemetry \
     -m "{\"device\":\"sensor-0001\",\"ts\":$(date +%s%3N),\"temperature\":21.7,\"humidity\":44.1}"
   ```

   Telegraf prints line protocol similar to:

   ```text
   sensor,device=sensor-0001,line=line1,topic=connectmq/demo/a1b2c3/line1/sensor-0001/telemetry humidity=44.1,temperature=21.7 1760600000123000000
   ```

5. Start Telegraf normally with `telegraf --config telegraf.conf` and query InfluxDB:

   ```bash
   influx query 'from(bucket: "sensors") |> range(start: -15m) |> filter(fn: (r) => r._measurement == "sensor") |> limit(n: 5)' \
     --org iot --token my-super-secret-token
   ```

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-telegraf-mqtt-consumer-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-telegraf-mqtt-consumer-private) — the **Serverless (Free)** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. Replace the `[[inputs.mqtt_consumer]]` block in `telegraf.conf` with the TLS version from the post and set `MQTT_USERNAME` / `MQTT_PASSWORD` as environment variables:

   ```toml
   [[inputs.mqtt_consumer]]
     servers = ["ssl://broker.connectmq.com:8883"]
     topics = ["connectmq/factory1/production/+/+/telemetry"]
     qos = 1
     client_id = "YOUR_CLIENT_ID"
     username = "${MQTT_USERNAME}"
     password = "${MQTT_PASSWORD}"
     persistent_session = true
     max_undelivered_messages = 1000

     name_override = "sensor"
     data_format = "json"
     tag_keys = ["device"]
     json_time_key = "ts"
     json_time_format = "unix_ms"
   ```

   The broker presents a Let's Encrypt certificate trusted by the OS CA store, so no `tls_ca` setting is needed.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [Telegraf MQTT Consumer: Ingest MQTT Data into InfluxDB](https://connectmq.com/blog/telegraf-mqtt-consumer/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-telegraf-mqtt-consumer-related) — the full tutorial with explanations
- 🧩 [Telegraf json_v2 parser tutorial](../telegraf-json-v2-parser/) · [TIG stack Docker Compose](../tig-stack-docker-compose/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-telegraf-mqtt-consumer-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-telegraf-mqtt-consumer-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-telegraf-mqtt-consumer-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-telegraf-mqtt-consumer-footer">Blog</a>
</p>
