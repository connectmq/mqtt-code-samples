# Build an MQTT Telegram Bot for Device Alerts and Commands

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-telegram-bot-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-telegram-bot-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Connect a Telegram bot to an MQTT broker with Python so alarms arrive in your chat and commands like /on, /off and /status travel back to devices, with a chat allowlist for safety.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-telegram-bot-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-telegram-bot-intro)

📖 **Full step-by-step tutorial:** [Build an MQTT Telegram Bot for Device Alerts and Commands](https://connectmq.com/blog/mqtt-telegram-bot/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-telegram-bot-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-telegram-bot-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`telegram_bot.py`](telegram_bot.py) | MQTT Telegram bot: forwards device alerts to allowlisted chats (with per-device cooldown) and publishes `/on`, `/off` commands; `/status` shows cached telemetry |
| [`requirements.txt`](requirements.txt) | `paho-mqtt>=2.0` and `requests` |
| [`systemd/telegram-mqtt-bot.service`](systemd/telegram-mqtt-bot.service) | systemd unit that runs the bot at boot and restarts it after crashes |
| [`systemd/telegram-mqtt-bot.env`](systemd/telegram-mqtt-bot.env) | Environment file template for the service (bot token, chat IDs, broker) |

## Requirements

- Python 3 with `paho-mqtt>=2.0` and `requests`
- A Telegram bot token from **@BotFather** and your numeric chat ID
- Optional: `mosquitto_pub` / `mosquitto_sub` to simulate a device
- Optional: a Linux host with systemd (e.g. Raspberry Pi) to run the bot as a service

## Run it on the free public broker

1. Create the bot with **@BotFather** (`/newbot`), send your bot any message, then find your chat ID:

   ```bash
   curl -s "https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates"
   ```

2. Install the dependencies:

   ```bash
   pip install "paho-mqtt>=2.0" requests
   ```

3. Run the bot:

   ```bash
   export TELEGRAM_BOT_TOKEN=YOUR_BOT_TOKEN
   export TELEGRAM_CHAT_IDS=123456789
   python telegram_bot.py
   ```

4. Simulate a device in another terminal: telemetry, an alert, then listen for commands:

   ```bash
   mosquitto_pub -h broker.connectmq.com -p 1883 -i tg-dev-9214 \
     -t connectmq/demo/tgbot-9214/pump1/telemetry -m '{"temp": 41.2, "running": true}'
   mosquitto_pub -h broker.connectmq.com -p 1883 -i tg-dev-9214 \
     -t connectmq/demo/tgbot-9214/pump1/alert -m '{"level": "high", "text": "Temperature above 80 C"}'
   mosquitto_sub -h broker.connectmq.com -p 1883 -i tg-listen-9214 -v \
     -t "connectmq/demo/tgbot-9214/+/cmd"
   ```

   Your phone shows `[HIGH] pump1: Temperature above 80 C`. Send `/status` and `/off pump1` to the bot. Pick your own random suffix instead of `tgbot-9214` (set `TOPIC_PREFIX`).

5. Optional — run as a systemd service: copy `systemd/telegram-mqtt-bot.env` to `/etc/telegram-mqtt-bot.env` and `systemd/telegram-mqtt-bot.service` to `/etc/systemd/system/`, then:

   ```bash
   sudo chmod 600 /etc/telegram-mqtt-bot.env
   sudo systemctl daemon-reload
   sudo systemctl enable --now telegram-mqtt-bot
   journalctl -u telegram-mqtt-bot -f
   ```

Never control real equipment through the public broker — anyone can publish to public topics.

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-telegram-bot-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-telegram-bot-private) — the **Serverless (Free)** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. No code changes are needed: `telegram_bot.py` reads the broker settings from the environment and enables TLS when the port is 8883. Set `MQTT_HOST`, `MQTT_PORT=8883`, `MQTT_USERNAME`, `MQTT_PASSWORD` and `MQTT_CLIENT_ID` (in your shell or in `/etc/telegram-mqtt-bot.env`):

   ```bash
   export MQTT_HOST=YOUR_BROKER_HOST
   export MQTT_PORT=8883
   export MQTT_USERNAME=YOUR_USERNAME
   export MQTT_PASSWORD=YOUR_PASSWORD
   export MQTT_CLIENT_ID=YOUR_CLIENT_ID
   ```

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [Build an MQTT Telegram Bot for Device Alerts and Commands](https://connectmq.com/blog/mqtt-telegram-bot/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-telegram-bot-related) — the full tutorial with explanations
- 🧩 [Python basic example](../../python/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-telegram-bot-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-telegram-bot-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-telegram-bot-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-telegram-bot-footer">Blog</a>
</p>
