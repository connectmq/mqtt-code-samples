# VS Code MQTT Extension: Publish and Subscribe Without Leaving Your Editor

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-vs-code-mqtt-extension-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-vs-code-mqtt-extension-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Set up MQTT inside VS Code with the ConnectMQ extension and a few workspace tasks, so you can connect to a broker, watch topics and publish test payloads next to the firmware or backend code you are writing.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-vs-code-mqtt-extension-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-vs-code-mqtt-extension-intro)

📖 **Full step-by-step tutorial:** [VS Code MQTT Extension: Publish and Subscribe Without Leaving Your Editor](https://connectmq.com/blog/vs-code-mqtt-extension/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-vs-code-mqtt-extension-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-vs-code-mqtt-extension-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`.vscode/tasks.json`](.vscode/tasks.json) | Workspace tasks: watch demo topics, publish a payload file (picked from a list), wait for one telemetry message as a smoke test |
| [`mqtt/payloads/telemetry-out-of-range.json`](mqtt/payloads/telemetry-out-of-range.json) | Edge-case telemetry payload with impossible values for testing backend validation |

The post's layout also lists `cmd-blink.json`, `cmd-reboot.json` and `telemetry-normal.json` in `mqtt/payloads/`, but does not show their contents; add your own (for example `cmd-blink.json` with `{"action": "blink", "times": 3}`, the command used in the post) before picking them in the publish task.

## Requirements

- Visual Studio Code with the **ConnectMQ** extension (Extensions view, `Ctrl+Shift+X` / `Cmd+Shift+X`, search for ConnectMQ)
- Mosquitto clients (`mosquitto_pub` / `mosquitto_sub`) for the workspace tasks

## Run it on the free public broker

1. In the extension, create a connection: host `broker.connectmq.com`, port 1883 (TCP) or 8883 (TLS), a unique client ID such as `vscode-7hq2`, username and password empty, MQTT 5.0 or 3.1.1.
2. Replace `7hq2` with your own random prefix in `.vscode/tasks.json`.
3. Subscribe to `connectmq/demo/7hq2/#`, then publish `{"action": "blink", "times": 3}` to `connectmq/demo/7hq2/device1/cmd` and confirm it arrives.
4. Open this folder in VS Code and run the tasks from **Terminal > Run Task**. They run these commands:

   ```bash
   # MQTT: watch demo topics
   mosquitto_sub -h broker.connectmq.com -p 1883 -i vscode-watch-7hq2 -t 'connectmq/demo/7hq2/#' -v

   # MQTT: publish payload file
   mosquitto_pub -h broker.connectmq.com -p 1883 -i vscode-pub-7hq2 -t connectmq/demo/7hq2/device1/telemetry -q 1 -f mqtt/payloads/telemetry-out-of-range.json

   # MQTT: wait for one telemetry message (fails if nothing arrives within 15 s)
   mosquitto_sub -h broker.connectmq.com -p 1883 -i vscode-check-7hq2 -t connectmq/demo/7hq2/device1/telemetry -C 1 -W 15
   ```

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-vs-code-mqtt-extension-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-vs-code-mqtt-extension-private) — the **Free** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. In the extension, set host to your broker host, port **8883 (TLS)**, client ID `YOUR_CLIENT_ID` and username/password `YOUR_USERNAME` / `YOUR_PASSWORD` (client IDs are bound to the issued credentials). In `.vscode/tasks.json`, change `-h`, use `-p 8883`, use the issued client ID with `-i`, and add credentials from environment variables instead of committing them:

   ```bash
   -u $MQTT_USER -P $MQTT_PASS
   ```

   On Windows PowerShell use `$env:MQTT_USER`. Alternatively keep the `-u` and `-P` lines in a Mosquitto client config file outside the repo (`~/.config/mosquitto_pub`).

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [VS Code MQTT Extension: Publish and Subscribe Without Leaving Your Editor](https://connectmq.com/blog/vs-code-mqtt-extension/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-vs-code-mqtt-extension-related) — the full tutorial with explanations
- 🧩 [CLI basic example](../../cli/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-vs-code-mqtt-extension-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-vs-code-mqtt-extension-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-vs-code-mqtt-extension-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-vs-code-mqtt-extension-footer">Blog</a>
</p>
