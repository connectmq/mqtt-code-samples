# Grafana MQTT Datasource: Live Streaming Panels from Your Broker

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-grafana-mqtt-datasource-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-grafana-mqtt-datasource-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Install and configure Grafana's MQTT data source plugin, stream numeric and JSON payloads from broker.connectmq.com into live panels, and decide when a time-series database such as InfluxDB is the better choice.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-grafana-mqtt-datasource-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-grafana-mqtt-datasource-intro)

📖 **Full step-by-step tutorial:** [Grafana MQTT Datasource: Live Streaming Panels from Your Broker](https://connectmq.com/blog/grafana-mqtt-datasource/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-grafana-mqtt-datasource-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-grafana-mqtt-datasource-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`docker-compose.yml`](docker-compose.yml) | Grafana 11.3.0 with the `grafana-mqtt-datasource` plugin installed at startup and a persistent data volume. |

## Requirements

- Docker with Docker Compose (or a native Grafana installation)
- The `grafana-mqtt-datasource` plugin
- `mosquitto_pub` and `awk` to publish test data
- Outbound access from the Grafana server to port 1883 or 8883

## Run it on the free public broker

1. Start Grafana with the plugin and open http://localhost:3000 (login `admin` / `admin`, then change it):

   ```bash
   docker compose up -d
   ```

   On a native installation instead:

   ```bash
   grafana cli plugins install grafana-mqtt-datasource
   sudo systemctl restart grafana-server
   ```

2. Go to Connections → Data sources → Add data source → MQTT, set the URI to `tcp://broker.connectmq.com:1883`, leave username and password empty, and click Save and test.
3. Publish test data with your own unique prefix. Plain numbers:

   ```bash
   ID=a1b2c3
   while true; do
     T=$(awk -v r=$RANDOM 'BEGIN { printf "%.2f", 20 + r / 32767 * 5 }')
     mosquitto_pub -h broker.connectmq.com -p 1883 -i "pub-$ID" \
       -t "connectmq/demo/$ID/room1/temperature" -m "$T"
     sleep 2
   done
   ```

   Or JSON with several values:

   ```bash
   ID=a1b2c3
   while true; do
     T=$(awk -v r=$RANDOM 'BEGIN { printf "%.2f", 20 + r / 32767 * 5 }')
     H=$(awk -v r=$RANDOM 'BEGIN { printf "%.1f", 40 + r / 32767 * 15 }')
     mosquitto_pub -h broker.connectmq.com -p 1883 -i "pubjson-$ID" \
       -t "connectmq/demo/$ID/room1/telemetry" \
       -m "{\"temperature\": $T, \"humidity\": $H}"
     sleep 2
   done
   ```

4. Create a dashboard, add a Time series visualization with the MQTT data source and enter the topic, e.g. `connectmq/demo/a1b2c3/room1/temperature`. Set the time range to the last 5 minutes; values stream in within seconds. For the JSON topic, `temperature` and `humidity` become two series.

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-grafana-mqtt-datasource-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-grafana-mqtt-datasource-private) — the **Free** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. In the MQTT data source settings, change:

   | Setting | Private broker |
   | --- | --- |
   | URI | `tls://broker.connectmq.com:8883` (or your broker host) |
   | Username | `YOUR_USERNAME` |
   | Password | `YOUR_PASSWORD` |
   | TLS options | Leave CA empty; the Let's Encrypt certificate is publicly trusted |

   If your plugin version shows a client ID field, enter the client ID issued with your username. The Grafana server connection counts toward your plan's connection limit.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [Grafana MQTT Datasource: Live Streaming Panels from Your Broker](https://connectmq.com/blog/grafana-mqtt-datasource/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-grafana-mqtt-datasource-related) — the full tutorial with explanations
- 🧩 [CLI basic example](../../cli/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-grafana-mqtt-datasource-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-grafana-mqtt-datasource-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-grafana-mqtt-datasource-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-grafana-mqtt-datasource-footer">Blog</a>
</p>
