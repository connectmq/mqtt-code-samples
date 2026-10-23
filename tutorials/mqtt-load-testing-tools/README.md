# MQTT Load Testing Tools: emqtt-bench, MQTTX Bench and Locust Compared

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-load-testing-tools-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-load-testing-tools-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

A practical comparison of emqtt-bench, MQTTX Bench and Locust for MQTT load testing, with real commands, a latency and loss probe in Python, the metrics worth collecting and the rules for testing responsibly against a private broker.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-load-testing-tools-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-load-testing-tools-intro)

📖 **Full step-by-step tutorial:** [MQTT Load Testing Tools: emqtt-bench, MQTTX Bench and Locust Compared](https://connectmq.com/blog/mqtt-load-testing-tools/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-load-testing-tools-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-load-testing-tools-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`locustfile.py`](locustfile.py) | Locust `User` class around paho-mqtt: each simulated device connects over TLS and publishes QoS 1 telemetry, reporting connect and PUBACK times to Locust |
| [`probe.py`](probe.py) | Latency and loss probe: publishes 600 sequenced, timestamped messages and prints received/lost counts and p50/p95/p99 latency |
| [`commands.sh`](commands.sh) | The post's emqtt-bench, MQTTX Bench and Locust commands, grouped by tool |
| [`requirements.txt`](requirements.txt) | Python packages for the Locust file and probe (`locust`, `paho-mqtt`) |

## Requirements

- A private MQTT broker you own or are explicitly allowed to test (never the shared public broker)
- [emqtt-bench](https://github.com/emqx/emqtt-bench) and/or MQTTX CLI (`mqttx bench`)
- Python 3 with `locust` and `paho-mqtt` for `locustfile.py` and `probe.py`

## Run it on the free public broker

**Do not load test the public broker.** `broker.connectmq.com` is a shared test service with strict per-client limits (10 messages per second per client, 10 subscriptions per client, 64 KB messages); a load test there measures those limits, not your system, and degrades it for everyone else. Use the public broker only to learn the tools, then run real tests against a private broker (next section).

1. Install the Python packages:

   ```bash
   pip install locust paho-mqtt
   ```

2. Validate credentials, TLS, topics and client ID rules with a single client first, then run the probe on an idle broker for a baseline:

   ```bash
   python probe.py
   ```

3. Ramp the load in stages with one of the tools (all commands are in `commands.sh`), for example:

   ```bash
   emqtt_bench pub -h YOUR_BROKER_HOST -p 1883 -c 200 -i 10 -I 1000 \
     -t 'loadtest/device/%i' -s 256 -q 1 -u YOUR_USERNAME -P YOUR_PASSWORD
   ```

   ```bash
   locust -f locustfile.py --headless -u 100 -r 5 --run-time 10m
   ```

4. Run `probe.py` again during each load stage; the difference from the baseline is what the load costs.

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-load-testing-tools-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-load-testing-tools-private) — the **Free** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. Create a dedicated broker for load testing so production devices are not affected, then set the environment variables that `locustfile.py` and `probe.py` read (both already use TLS on port 8883 with `tls_set()`):

   ```bash
   export MQTT_HOST=YOUR_BROKER_HOST
   export MQTT_USER=YOUR_USERNAME
   export MQTT_PASS=YOUR_PASSWORD
   ```

   In `commands.sh`, replace `YOUR_BROKER_HOST`, `YOUR_USERNAME` and `YOUR_PASSWORD`; for emqtt-bench add `--ssl` and use port 8883 to test TLS. If your credentials only allow specific client IDs, configure the tool's client ID option (or the generated IDs in the Python files) to match. Know your plan's quotas: MQTT 5 clients receive reason code 0x97 (quota exceeded) when a plan limit is reached.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [MQTT Load Testing Tools: emqtt-bench, MQTTX Bench and Locust Compared](https://connectmq.com/blog/mqtt-load-testing-tools/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-load-testing-tools-related) — the full tutorial with explanations
- 🧩 [CLI basic example](../../cli/)
- 🧩 [Python basic example](../../python/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-load-testing-tools-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-load-testing-tools-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-load-testing-tools-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-load-testing-tools-footer">Blog</a>
</p>
