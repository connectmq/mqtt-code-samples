# PHP MQTT Client Tutorial with php-mqtt/client

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-php-mqtt-client-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-php-mqtt-client-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Learn to publish MQTT messages from a PHP web request and run a long-lived PHP subscriber worker with php-mqtt/client, including TLS, reconnects, graceful shutdown and Laravel-friendly patterns.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-php-mqtt-client-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-php-mqtt-client-intro)

📖 **Full step-by-step tutorial:** [PHP MQTT Client Tutorial with php-mqtt/client](https://connectmq.com/blog/php-mqtt-client/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-php-mqtt-client-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-php-mqtt-client-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`mqtt.php`](mqtt.php) | Shared connection settings: host, TLS on port 8883, optional credentials and auto-reconnect from environment variables |
| [`public/command.php`](public/command.php) | Web endpoint that publishes an `on`/`off` command to a device with QoS 1 and waits for the PUBACK |
| [`bin/subscriber.php`](bin/subscriber.php) | Long-lived CLI worker that subscribes to `devices/+/telemetry`, decodes JSON and shuts down cleanly on SIGTERM |
| [`systemd/php-mqtt-worker.service`](systemd/php-mqtt-worker.service) | systemd unit that keeps the subscriber running (install as `/etc/systemd/system/php-mqtt-worker.service`) |
| [`systemd/php-mqtt-worker.env`](systemd/php-mqtt-worker.env) | Environment file with private broker credentials (install as `/etc/php-mqtt-worker.env`, mode 600) |

## Requirements

- PHP CLI with the standard sockets and OpenSSL support
- [Composer](https://getcomposer.org/) and the [`php-mqtt/client`](https://github.com/php-mqtt/client) package (MQTT 3.1 / 3.1.1)
- The `pcntl` extension for the subscriber (available in the PHP CLI on Linux, usually not under PHP-FPM or on Windows)
- `mosquitto_pub` to simulate a device
- Optional: systemd (or Supervisor / a container runtime) to run the worker in production

## Run it on the free public broker

1. Install the client library:

   ```bash
   composer require php-mqtt/client
   ```

2. Start the subscriber worker:

   ```bash
   php bin/subscriber.php
   ```

3. In another terminal, act as a device:

   ```bash
   mosquitto_pub -h broker.connectmq.com -p 1883 -i php-sim-pump1 \
     -t "connectmq/demo/php-5e19c2/devices/pump1/telemetry" \
     -m '{"flow": 12.4, "pressure": 2.1}'
   ```

4. Serve `public/command.php` from your web server and POST `device` (e.g. `pump1`) and `action` (`on` or `off`) to it to publish a command to `connectmq/demo/php-5e19c2/devices/<device>/set`.

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-php-mqtt-client-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-php-mqtt-client-private) — the **Free** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. The code already uses TLS on port 8883. Set `MQTT_HOST` in `mqtt.php` to your broker host, and provide the credentials as environment variables — `mqtt.php` switches to them automatically when `MQTT_USERNAME` is set. For the systemd worker, put them in `/etc/php-mqtt-worker.env` (mode 600):

   ```bash
   MQTT_USERNAME=YOUR_USERNAME
   MQTT_PASSWORD=YOUR_PASSWORD
   MQTT_CLIENT_ID=YOUR_CLIENT_ID
   MQTT_TOPIC_PREFIX=acme/site1
   ```

   Use a different credential set / client ID for the web publisher and the worker: client IDs are bound to the credentials you are issued, and two processes sharing one kick each other off.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [PHP MQTT Client Tutorial with php-mqtt/client](https://connectmq.com/blog/php-mqtt-client/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-php-mqtt-client-related) — the full tutorial with explanations
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-php-mqtt-client-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-php-mqtt-client-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-php-mqtt-client-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-php-mqtt-client-footer">Blog</a>
</p>
