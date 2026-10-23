# MQTT to MongoDB: Save Device Messages with Node.js and Time-Series Collections

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-mongodb-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-mongodb-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Build an MQTT to MongoDB pipeline with Node.js: an MQTT.js subscriber validates device messages and batches them into a MongoDB time-series collection with automatic expiry and aggregation-ready indexes.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-mongodb-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-mongodb-intro)

📖 **Full step-by-step tutorial:** [MQTT to MongoDB: Save Device Messages with Node.js and Time-Series Collections](https://connectmq.com/blog/mqtt-to-mongodb/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-mongodb-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-mongodb-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`setup.mjs`](setup.mjs) | Creates the `iot.telemetry` time-series collection (90-day expiry) and a `meta.deviceId` + `ts` index |
| [`subscriber.mjs`](subscriber.mjs) | MQTT.js subscriber with a persistent session that validates JSON telemetry and batches it into MongoDB with `insertMany` |
| [`package.json`](package.json) | Node.js project with the `mqtt` and `mongodb` dependencies |

## Requirements

- Node.js 20+
- MQTT.js 5 (`mqtt`) and the MongoDB Node.js driver 6 (`mongodb`)
- MongoDB 7 (e.g. via Docker)
- `mosquitto_pub` to simulate devices, `mongosh` to inspect the data

## Run it on the free public broker

1. Start MongoDB:

   ```bash
   docker run -d --name mongo -p 27017:27017 \
     -v mongo-data:/data/db \
     mongo:7
   ```

2. Install the packages and create the time-series collection:

   ```bash
   npm install mqtt mongodb
   node setup.mjs
   ```

3. Run the subscriber and publish test readings from another terminal (devices publish to `<prefix>/<site>/<deviceId>/telemetry`):

   ```bash
   node subscriber.mjs

   # in another terminal
   for i in $(seq 1 30); do
     mosquitto_pub -h broker.connectmq.com -p 1883 -i mongo-sim-01 -q 1 \
       -t "connectmq/demo/mongo-9d42a7/plant1/sensor-01/telemetry" \
       -m "{\"temperature\": 2$((RANDOM % 10)).$((RANDOM % 10)), \"humidity\": 4$((RANDOM % 10))}"
     sleep 1
   done
   ```

4. Look at the data in `mongosh`:

   ```javascript
   use iot
   db.telemetry.find().sort({ ts: -1 }).limit(3)
   ```

5. Per-minute averages for one device over the last 24 hours:

   ```javascript
   db.telemetry.aggregate([
     { $match: { "meta.deviceId": "sensor-01", ts: { $gte: new Date(Date.now() - 864e5) } } },
     { $group: {
         _id: { $dateTrunc: { date: "$ts", unit: "minute" } },
         avgTemp: { $avg: "$temperature" },
         maxTemp: { $max: "$temperature" },
         samples: { $sum: 1 }
     } },
     { $sort: { _id: 1 } }
   ])
   ```

   Latest reading per device:

   ```javascript
   db.telemetry.aggregate([
     { $sort: { "meta.deviceId": 1, ts: -1 } },
     { $group: { _id: "$meta.deviceId", last: { $first: "$$ROOT" } } }
   ])
   ```

Use your own suffix instead of `mongo-9d42a7` (set `MQTT_TOPIC_PREFIX`) and set a fixed `MQTT_CLIENT_ID` so the persistent session survives restarts.

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-mongodb-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-mongodb-private) — the **Free** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. No code changes are needed: `subscriber.mjs` reads the broker URL and credentials from the environment. Keep `mqtts://` on port 8883 and set the generated values:

   ```bash
   export MQTT_URL=mqtts://YOUR_BROKER_HOST:8883
   export MQTT_USERNAME=YOUR_USERNAME
   export MQTT_PASSWORD=YOUR_PASSWORD
   export MQTT_CLIENT_ID=YOUR_CLIENT_ID
   ```

   Give the subscriber its own credentials (two processes with one client ID disconnect each other) and use a MongoDB user with insert rights on `iot.telemetry` only.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [MQTT to MongoDB: Save Device Messages with Node.js and Time-Series Collections](https://connectmq.com/blog/mqtt-to-mongodb/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-mongodb-related) — the full tutorial with explanations
- 🧩 [Node.js basic example](../../nodejs/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-mongodb-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-mongodb-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-mongodb-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-mongodb-footer">Blog</a>
</p>
