# Telegraf json_v2 Parser and MQTT Topic Parsing Explained

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-telegraf-json-v2-parser-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-telegraf-json-v2-parser-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

How to turn real MQTT payloads into clean InfluxDB metrics with Telegraf: json_v2 fields, tags, renames and types for nested JSON, object parsing for arrays, and topic_parsing to extract site, line and machine from the topic.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-telegraf-json-v2-parser-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-telegraf-json-v2-parser-intro)

📖 **Full step-by-step tutorial:** [Telegraf json_v2 Parser and MQTT Topic Parsing Explained](https://connectmq.com/blog/telegraf-json-v2-parser/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-telegraf-json-v2-parser-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-telegraf-json-v2-parser-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`json_v2.conf`](json_v2.conf) | Telegraf config: `mqtt_consumer` with `topic_parsing` and a `json_v2` mapping of a nested machine payload, printed as line protocol to stdout |

## Requirements

- Telegraf (a version with the `json_v2` parser and `topic_parsing` support)
- `mosquitto_pub` / `mosquitto_sub` (Mosquitto clients) to publish test payloads
- Optional: InfluxDB 2.x for production output

## Run it on the free public broker

1. Replace `a1b2c3` in `json_v2.conf` with your own random ID (topics and `client_id`).
2. Start Telegraf in test mode. `mqtt_consumer` is a service input, so it waits for a message:

   ```bash
   telegraf --config json_v2.conf --test --test-wait 20
   ```

3. While it waits, publish the test payload:

   ```bash
   mosquitto_pub -h broker.connectmq.com -p 1883 -i pub-a1b2c3 \
     -t connectmq/demo/a1b2c3/factory1/line1/cnc1/telemetry \
     -m "{\"ts\":$(date +%s%3N),\"device\":{\"id\":\"cnc1\",\"fw\":\"2.4.1\",\"serial\":\"SN-88231\"},\"status\":\"running\",\"metrics\":{\"spindle_rpm\":11800,\"temp_c\":41.7,\"vibration_mm_s\":2.3},\"alarms\":[]}"
   ```

   Expected output (one line of line protocol):

   ```text
   machine,asset=cnc1,firmware=2.4.1,line=line1,site=factory1 status="running",spindle_rpm=11800i,temp_c=41.7,vibration_mm_s=2.3,alarm_count=0i 1760600000123000000
   ```

4. No output? Check the topic:

   ```bash
   mosquitto_sub -h broker.connectmq.com -p 1883 -i dbg-a1b2c3 -t "connectmq/demo/a1b2c3/#" -v
   ```

### Variation: measurement from the topic

Replace the `topic_parsing` block with this one to take the measurement name from the last topic level (`telemetry`, `energy`, ...):

```toml
  [[inputs.mqtt_consumer.topic_parsing]]
    topic = "connectmq/demo/a1b2c3/+/+/+/+"
    measurement = "_/_/_/_/_/_/measurement"
    tags = "_/_/_/site/line/asset/_"
```

### Variation: parsing arrays into multiple metrics

For batched gateway payloads with a `readings` array, add a second `mqtt_consumer` input that listens on the batch topic:

```toml
[[inputs.mqtt_consumer]]
  servers = ["tcp://broker.connectmq.com:1883"]
  topics = ["connectmq/demo/a1b2c3/+/+/+/batch"]
  client_id = "telegraf-batch-a1b2c3"
  topic_tag = ""
  data_format = "json_v2"

  [[inputs.mqtt_consumer.topic_parsing]]
    topic = "connectmq/demo/a1b2c3/+/+/+/batch"
    tags = "_/_/_/site/line/gateway/_"

  [[inputs.mqtt_consumer.json_v2]]
    measurement_name = "reading"

    [[inputs.mqtt_consumer.json_v2.object]]
      path = "readings"
      tags = ["sensor"]
      timestamp_key = "ts"
      timestamp_format = "unix_ms"
      [inputs.mqtt_consumer.json_v2.object.fields]
        value = "float"
```

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-telegraf-json-v2-parser-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-telegraf-json-v2-parser-private) — the **Serverless (Free)** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. In `json_v2.conf`, switch the `[[inputs.mqtt_consumer]]` to TLS and add the credentials and client ID issued in the portal. For production, also replace the `[[outputs.file]]` block with an `[[outputs.influxdb_v2]]` output:

   ```toml
   [[inputs.mqtt_consumer]]
     servers = ["ssl://broker.connectmq.com:8883"]
     username = "YOUR_USERNAME"
     password = "YOUR_PASSWORD"
     client_id = "YOUR_CLIENT_ID"
   ```

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [Telegraf json_v2 Parser and MQTT Topic Parsing Explained](https://connectmq.com/blog/telegraf-json-v2-parser/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-telegraf-json-v2-parser-related) — the full tutorial with explanations
- 🧩 [Telegraf MQTT consumer tutorial](../telegraf-mqtt-consumer/) · [TIG stack Docker Compose](../tig-stack-docker-compose/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-telegraf-json-v2-parser-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-telegraf-json-v2-parser-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-telegraf-json-v2-parser-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-telegraf-json-v2-parser-footer">Blog</a>
</p>
