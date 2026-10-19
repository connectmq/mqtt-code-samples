# Ruby MQTT Client Tutorial: Publish, Subscribe and TLS with the mqtt Gem

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-ruby-mqtt-client-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-ruby-mqtt-client-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

A practical Ruby MQTT client tutorial using the mqtt gem: publish and subscribe, verified TLS, a reconnecting subscriber loop, and patterns for publishing from Rails and running a worker alongside it.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-ruby-mqtt-client-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-ruby-mqtt-client-intro)

📖 **Full step-by-step tutorial:** [Ruby MQTT Client Tutorial: Publish, Subscribe and TLS with the mqtt Gem](https://connectmq.com/blog/ruby-mqtt-client/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-ruby-mqtt-client-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-ruby-mqtt-client-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`hello.rb`](hello.rb) | First publish/subscribe test on port 1883: a subscriber thread and a publisher that sends `hello from Ruby` and `bye` |
| [`tls_client.rb`](tls_client.rb) | `build_client` helper: TLS on 8883 with `VERIFY_PEER`, credentials and client ID from environment variables; publishes a test status when run directly |
| [`mqtt_worker.rb`](mqtt_worker.rb) | `MqttWorker`: reconnecting subscriber with exponential backoff, JSON handling and clean shutdown on INT/TERM |
| [`rails/app/services/device_commands.rb`](rails/app/services/device_commands.rb) | Rails service object that validates the device ID and publishes a command at QoS 1 |
| [`rails/app/jobs/device_command_job.rb`](rails/app/jobs/device_command_job.rb) | ActiveJob that calls `DeviceCommands.send!` in the background |
| [`rails/bin/mqtt_worker`](rails/bin/mqtt_worker) | Runner script that boots Rails and stores incoming telemetry with `Reading.create!` |
| [`rails/Procfile`](rails/Procfile) | Runs the web server and the MQTT worker as separate process types |

For a Rails app, copy `tls_client.rb` and `mqtt_worker.rb` into `lib/` and the files under `rails/` into the matching paths of your app.

## Requirements

- Ruby (the `mqtt` gem is pure Ruby, MQTT 3.1.1 only)
- The [`mqtt` gem](https://github.com/njh/ruby-mqtt)
- Ruby's OpenSSL with a CA bundle (install `ca-certificates` in slim Docker images)
- Optional: Rails with ActiveJob and a `Reading` model for the Rails parts
- `mosquitto_pub` to simulate a device

## Run it on the free public broker

1. Install the gem:

   ```bash
   gem install mqtt
   # or in a Rails app
   bundle add mqtt
   ```

2. Run the first publish/subscribe test:

   ```bash
   ruby hello.rb
   ```

3. Publish over verified TLS on port 8883:

   ```bash
   ruby tls_client.rb
   ```

4. Start the reconnecting worker and simulate a device:

   ```bash
   ruby mqtt_worker.rb

   # in another terminal
   mosquitto_pub -h broker.connectmq.com -p 1883 -i ruby-sim-boiler \
     -t "connectmq/demo/ruby-worker-7c2e/devices/boiler1/telemetry" \
     -m '{"temp": 71.5, "burner": true}'
   ```

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-ruby-mqtt-client-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-ruby-mqtt-client-private) — the **Serverless (Free)** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. `tls_client.rb` already uses TLS on 8883 with `VERIFY_PEER` and reads everything from the environment, so `tls_client.rb`, `mqtt_worker.rb` and the Rails files need no code change. Set (in Rails credentials or your platform's secret store):

   ```bash
   MQTT_HOST=YOUR_BROKER_HOST
   MQTT_USERNAME=YOUR_USERNAME
   MQTT_PASSWORD=YOUR_PASSWORD
   MQTT_CLIENT_ID=YOUR_CLIENT_ID
   MQTT_TOPIC_PREFIX=YOUR_TOPIC_PREFIX
   ```

   Client IDs are bound to issued credentials: run exactly one worker per client ID, and in `DeviceCommands` use the exact client ID you were given instead of a random suffix (or route all publishing through a single worker).

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [Ruby MQTT Client Tutorial: Publish, Subscribe and TLS with the mqtt Gem](https://connectmq.com/blog/ruby-mqtt-client/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-ruby-mqtt-client-related) — the full tutorial with explanations
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-ruby-mqtt-client-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-ruby-mqtt-client-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-ruby-mqtt-client-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-ruby-mqtt-client-footer">Blog</a>
</p>
