# MQTT to REST API Flask Tutorial: Expose Live Device Data over HTTP

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-rest-api-flask-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-rest-api-flask-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Build a Flask app that subscribes to MQTT topics, caches the latest value per device, serves it through REST endpoints and publishes commands from a POST route, with the deployment pitfalls that break most first attempts.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-rest-api-flask-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-rest-api-flask-intro)

📖 **Full step-by-step tutorial:** [MQTT to REST API Flask Tutorial: Expose Live Device Data over HTTP](https://connectmq.com/blog/mqtt-to-rest-api-flask/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-rest-api-flask-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-rest-api-flask-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`app.py`](app.py) | Flask bridge: caches the latest MQTT state per device and serves `GET /api/devices`, `GET /api/devices/<id>`, `POST /api/devices/<id>/command` and `GET /health` |
| [`requirements.txt`](requirements.txt) | `flask>=3.0` and `paho-mqtt>=2.0` |

## Requirements

- Python 3.9+
- `flask>=3.0` and `paho-mqtt>=2.0`
- `mosquitto_pub` / `mosquitto_sub` and `curl` for testing

## Run it on the free public broker

1. Install the dependencies:

   ```bash
   pip install "flask>=3.0" "paho-mqtt>=2.0"
   ```

2. Start the app:

   ```bash
   export API_KEY=dev-secret
   python app.py
   ```

3. Publish a retained state message as a device would:

   ```bash
   mosquitto_pub -h broker.connectmq.com -p 1883 -i flask-dev-3391 -r -q 1 \
     -t connectmq/demo/flask-3391/valve7/state -m '{"open": true, "flow": 12.4}'
   ```

4. Query and command through HTTP:

   ```bash
   curl -s -H "X-API-Key: dev-secret" http://localhost:5000/api/devices
   curl -s -H "X-API-Key: dev-secret" http://localhost:5000/api/devices/valve7
   curl -s -X POST -H "X-API-Key: dev-secret" -H "Content-Type: application/json" \
     -d '{"action": "close"}' http://localhost:5000/api/devices/valve7/command
   ```

5. Watch the command arrive:

   ```bash
   mosquitto_sub -h broker.connectmq.com -p 1883 -i flask-sub-3391 -v -t "connectmq/demo/flask-3391/+/cmd"
   ```

   When you are done, clear the retained test message by publishing an empty retained payload to the same topic. Use your own suffix instead of `flask-3391` (set `TOPIC_PREFIX`).

For deployment, keep `use_reloader=False` and run a single worker with threads: `gunicorn -w 1 --threads 8 app:app`.

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-rest-api-flask-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-rest-api-flask-private) — the **Serverless (Free)** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. No code changes are needed: `app.py` reads the broker settings from the environment and enables TLS when the port is 8883:

   ```bash
   export MQTT_HOST=YOUR_BROKER_HOST
   export MQTT_PORT=8883
   export MQTT_USERNAME=YOUR_USERNAME
   export MQTT_PASSWORD=YOUR_PASSWORD
   export MQTT_CLIENT_ID=YOUR_CLIENT_ID
   ```

   Also set a strong `API_KEY` and put the app behind HTTPS for anything internet-facing.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [MQTT to REST API Flask Tutorial: Expose Live Device Data over HTTP](https://connectmq.com/blog/mqtt-to-rest-api-flask/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-rest-api-flask-related) — the full tutorial with explanations
- 🧩 [Python basic example](../../python/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-rest-api-flask-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-rest-api-flask-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-rest-api-flask-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-to-rest-api-flask-footer">Blog</a>
</p>
