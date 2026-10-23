# Grafana Alerts for IoT Sensor Data: Thresholds, Stale Sensors and Notifications

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-grafana-alerts-iot-sensor-data-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-grafana-alerts-iot-sensor-data-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Build Grafana alert rules on MQTT sensor data in InfluxDB, with one alert instance per device, sensible pending periods, no-data handling for silent sensors and contact points, then compare them with broker-side threshold rules in ConnectMQ.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-grafana-alerts-iot-sensor-data-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-grafana-alerts-iot-sensor-data-intro)

📖 **Full step-by-step tutorial:** [Grafana Alerts for IoT Sensor Data: Thresholds, Stale Sensors and Notifications](https://connectmq.com/blog/grafana-alerts-iot-sensor-data/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-grafana-alerts-iot-sensor-data-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-grafana-alerts-iot-sensor-data-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`high-temperature.flux`](high-temperature.flux) | Query A for the "High temperature" rule: last 10 minutes of temperatures, one series per device, 1-minute means. |
| [`stale-sensor.flux`](stale-sensor.flux) | Query A for the stale-sensor rule: seconds since each device's last reading. |

## Requirements

- The TIG stack from the [TIG stack with Docker Compose tutorial](https://connectmq.com/blog/tig-stack-docker-compose/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-grafana-alerts-iot-sensor-data-intro): Telegraf subscribed to `broker.connectmq.com`, InfluxDB 2 and Grafana 10 or 11
- Data model: bucket `sensors`, measurement `sensor`, tags `device` and `line`, fields `temperature` and `humidity`, topics `connectmq/demo/<run-id>/<line>/<device>/telemetry`
- A contact point (Slack, Teams, Telegram, webhook or email via SMTP)
- `mosquitto_pub` to test the alerts

## Run it on the free public broker

1. **High temperature rule.** In Grafana open Alerting → Alert rules → New alert rule. Paste [`high-temperature.flux`](high-temperature.flux) as Query A (InfluxDB, Flux). Add expression B = Reduce (Last, "Drop non-numeric values") of A and expression C = Threshold (B is above 30) as the condition. Folder `IoT`, label `severity=warning`, evaluation group `sensors-1m` (1 minute), pending period 5 minutes. Summary annotation:

   ```text
   {{ $labels.device }} on {{ $labels.line }} is at {{ printf "%.1f" $values.B.Value }} °C
   ```

2. **Stale sensor rule.** New rule with [`stale-sensor.flux`](stale-sensor.flux) as Query A, Reduce Last as B, Threshold "is above 120" as C, pending period 2 minutes, and no-data handling set to Alerting.
3. **Routing.** Create a contact point, then a notification policy matching `severity=warning`, grouped by `alertname` and `line`. For email with Docker, add SMTP settings to the Grafana service:

   ```yaml
   services:
     grafana:
       environment:
         GF_SMTP_ENABLED: "true"
         GF_SMTP_HOST: smtp.example.com:587
         GF_SMTP_USER: alerts@example.com
         GF_SMTP_PASSWORD: ${SMTP_PASSWORD}
         GF_SMTP_FROM_ADDRESS: alerts@example.com
         GF_SMTP_FROM_NAME: IoT Alerts
   ```

4. **Test end to end.** Publish elevated readings for one test device:

   ```bash
   ID=a1b2c3
   for i in $(seq 1 60); do
     mosquitto_pub -h broker.connectmq.com -p 1883 -i "alerttest-$ID" \
       -t "connectmq/demo/$ID/line1/sensor-test/telemetry" \
       -m "{\"device\":\"sensor-test\",\"ts\":$(date +%s%3N),\"temperature\":35.5,\"humidity\":40.0}"
     sleep 10
   done
   ```

   The `sensor-test` instance goes Pending, then Firing after 5 minutes. Stop the loop: the high-temperature alert resolves and, two quiet minutes later, the stale-sensor rule fires.

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-grafana-alerts-iot-sensor-data-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-grafana-alerts-iot-sensor-data-private) — the **Free** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. The alert rules and Flux queries stay the same; only the ingestion side changes. In Telegraf's `[[inputs.mqtt_consumer]]` section, point `servers` at `ssl://YOUR_BROKER_HOST:8883` and set `username = "YOUR_USERNAME"`, `password = "YOUR_PASSWORD"` and `client_id = "YOUR_CLIENT_ID"`. For the test loop, add `-p 8883 -u YOUR_USERNAME -P YOUR_PASSWORD -i YOUR_CLIENT_ID_test` plus `--capath /etc/ssl/certs` to `mosquitto_pub`. The portal's threshold alert rules can cover simple thresholds while devices are commissioned.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [Grafana Alerts for IoT Sensor Data: Thresholds, Stale Sensors and Notifications](https://connectmq.com/blog/grafana-alerts-iot-sensor-data/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-grafana-alerts-iot-sensor-data-related) — the full tutorial with explanations
- 🧩 [CLI basic example](../../cli/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-grafana-alerts-iot-sensor-data-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-grafana-alerts-iot-sensor-data-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-grafana-alerts-iot-sensor-data-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-grafana-alerts-iot-sensor-data-footer">Blog</a>
</p>
