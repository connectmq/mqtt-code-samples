# Async MQTT in Python with aiomqtt and asyncio: Tasks, Workers and Reconnects

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-aiomqtt-asyncio-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-aiomqtt-asyncio-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Write asynchronous MQTT clients in Python with aiomqtt and asyncio: publish and subscribe without callbacks, run concurrent tasks with TaskGroup, process messages in worker queues and reconnect gracefully.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-aiomqtt-asyncio-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-aiomqtt-asyncio-intro)

📖 **Full step-by-step tutorial:** [Async MQTT in Python with aiomqtt and asyncio: Tasks, Workers and Reconnects](https://connectmq.com/blog/aiomqtt-asyncio/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-aiomqtt-asyncio-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-aiomqtt-asyncio-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`minimal_example.py`](minimal_example.py) | Smallest aiomqtt client: subscribes, publishes one message to itself and prints it. |
| [`aio_client.py`](aio_client.py) | Realistic async client: periodic publisher, consumer with a worker queue, Last Will and reconnect loop. |
| [`requirements.txt`](requirements.txt) | Python dependency (`aiomqtt>=2.0`). |

## Requirements

- Python 3.11 or newer (the examples use `asyncio.TaskGroup` and `except*`)
- aiomqtt 2.0 or newer
- Optional: `mosquitto_pub` to send test commands
- On Windows the code runs on a selector event loop (the default Proactor loop lacks `add_reader`/`add_writer`)

## Run it on the free public broker

1. Create a virtual environment and install aiomqtt:

   ```bash
   python -m venv .venv
   source .venv/bin/activate          # Windows: .venv\Scripts\activate
   pip install "aiomqtt>=2.0"
   ```

2. Pick your own random topic prefix and set `PREFIX` in both files (the examples use `connectmq/demo/k7f3q2`).
3. Run the minimal example, then the full client:

   ```bash
   python minimal_example.py
   python aio_client.py
   ```

   Every two seconds a reading is published, received back through the subscription and processed by one of the three workers.

4. Send a command from another terminal:

   ```bash
   mosquitto_pub -h broker.connectmq.com -p 1883 -i aio-cmd-test -t 'connectmq/demo/k7f3q2/commands/led' -m 'on'
   ```

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-aiomqtt-asyncio-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-aiomqtt-asyncio-private) — the **Free** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. In `aio_client.py`, set `BROKER` to your broker host and `PORT = 8883`, add `import ssl` at the top, and enable the commented lines in the `aiomqtt.Client(...)` call:

   ```python
   # Private ConnectMQ broker:
   # username="YOUR_USERNAME", password="YOUR_PASSWORD",
   # tls_context=ssl.create_default_context(), and port 8883
   ```

   Use the client ID generated in the dashboard as `identifier` (`CLIENT_ID`).

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [Async MQTT in Python with aiomqtt and asyncio: Tasks, Workers and Reconnects](https://connectmq.com/blog/aiomqtt-asyncio/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-aiomqtt-asyncio-related) — the full tutorial with explanations
- 🧩 [Python basic example](../../python/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-aiomqtt-asyncio-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-aiomqtt-asyncio-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-aiomqtt-asyncio-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-aiomqtt-asyncio-footer">Blog</a>
</p>
