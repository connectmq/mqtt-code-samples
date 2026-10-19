# MQTT Email Alerts Python Tutorial: Rate-Limited SMTP Notifications

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-email-alerts-python-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-email-alerts-python-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Build a Python service that subscribes to MQTT alarm and telemetry topics, applies thresholds with hysteresis and cooldowns, and sends rate-limited SMTP emails, then see how it complements ConnectMQ's built-in alert rules.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-email-alerts-python-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-email-alerts-python-intro)

📖 **Full step-by-step tutorial:** [MQTT Email Alerts Python Tutorial: Rate-Limited SMTP Notifications](https://connectmq.com/blog/mqtt-email-alerts-python/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-email-alerts-python-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-email-alerts-python-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`mqtt_email_alerts.py`](mqtt_email_alerts.py) | Subscribes to `<prefix>/+/telemetry` and `<prefix>/+/alarm`, applies thresholds with hysteresis and a per-device cooldown, and sends alert / resolved / alarm emails over SMTP from a worker thread with retries |
| [`requirements.txt`](requirements.txt) | Python dependency (`paho-mqtt>=2.0`) |

## Requirements

- Python 3 with `paho-mqtt` 2.x (`smtplib` and `email` are in the standard library)
- An SMTP server that accepts authenticated submissions: host and port (`587` STARTTLS or `465` implicit TLS), username and password (an app password with two-factor authentication), and an allowed sender address
- Optionally, `mosquitto_pub` for testing

## Run it on the free public broker

1. Install the dependency:

   ```bash
   pip install "paho-mqtt>=2.0"
   ```

2. Set your SMTP settings as environment variables and start the service (it listens under `connectmq/demo/mail-6630` by default; set `TOPIC_PREFIX` to your own random prefix):

   ```bash
   export SMTP_HOST=smtp.example.com SMTP_PORT=587
   export SMTP_USER=alerts@example.com SMTP_PASS='app-password'
   export MAIL_TO=you@example.com
   python mqtt_email_alerts.py
   ```

3. Publish a value over the limit, then a recovered value, then a device alarm:

   ```bash
   mosquitto_pub -h broker.connectmq.com -p 1883 -i mail-pub-6630 \
     -t connectmq/demo/mail-6630/oven2/telemetry -m '{"temperature": 84.1}'
   mosquitto_pub -h broker.connectmq.com -p 1883 -i mail-pub-6630 \
     -t connectmq/demo/mail-6630/oven2/telemetry -m '{"temperature": 72.0}'
   mosquitto_pub -h broker.connectmq.com -p 1883 -i mail-pub-6630 \
     -t connectmq/demo/mail-6630/oven2/alarm -m '{"severity": "critical", "text": "Door open"}'
   ```

   You should receive three emails: an alert, a resolution, and the critical alarm.

Other settings: `MAIL_FROM` (defaults to `SMTP_USER`), `COOLDOWN_MINUTES` (default 15). Thresholds live in the `THRESHOLDS` dictionary in the script.

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-email-alerts-python-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-email-alerts-python-private) — the **Serverless (Free)** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. Set the MQTT environment variables read by `mqtt_email_alerts.py` (TLS is enabled automatically when `MQTT_PORT` is `8883`), then start it as before:

   ```bash
   export MQTT_HOST=YOUR_BROKER_HOST
   export MQTT_PORT=8883
   export MQTT_USERNAME=YOUR_USERNAME
   export MQTT_PASSWORD=YOUR_PASSWORD
   export MQTT_CLIENT_ID=YOUR_CLIENT_ID
   export TOPIC_PREFIX=YOUR_TOPIC_PREFIX
   python mqtt_email_alerts.py
   ```

   Keep the process alive with systemd or a container restart policy.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [MQTT Email Alerts Python Tutorial: Rate-Limited SMTP Notifications](https://connectmq.com/blog/mqtt-email-alerts-python/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-email-alerts-python-related) — the full tutorial with explanations
- 🧩 [Python basic example](../../python/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-email-alerts-python-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-email-alerts-python-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-email-alerts-python-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-email-alerts-python-footer">Blog</a>
</p>
