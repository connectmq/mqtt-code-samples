# Testing MQTT Clients: Unit, Integration and End-to-End Tests

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-testing-mqtt-clients-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-testing-mqtt-clients-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

How to test MQTT client code at every level: pure unit tests with mocks, integration tests against a containerised Mosquitto broker in CI, and end-to-end smoke tests against a real cloud broker.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-testing-mqtt-clients-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-testing-mqtt-clients-intro)

📖 **Full step-by-step tutorial:** [Testing MQTT Clients: Unit, Integration and End-to-End Tests](https://connectmq.com/blog/testing-mqtt-clients/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-testing-mqtt-clients-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-testing-mqtt-clients-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`thermostat.py`](thermostat.py) | Testable business logic: a thermostat with hysteresis that takes an injected `publish` function |
| [`adapter.py`](adapter.py) | Thin paho-mqtt adapter that wires the thermostat to a broker and exposes a `ready` event |
| [`test_thermostat.py`](test_thermostat.py) | Unit tests with a mocked `publish` (no broker needed) |
| [`test_integration.py`](test_integration.py) | Integration tests against a local Mosquitto container (heater command, retained message) |
| [`smoke_test.py`](smoke_test.py) | End-to-end TLS smoke test against a real broker (publishes a nonce and waits for the echo) |
| [`.github/workflows/tests.yml`](.github/workflows/tests.yml) | GitHub Actions workflow that starts a Mosquitto container and runs pytest (copy it to your repo's root `.github/workflows/`) |
| [`requirements.txt`](requirements.txt) | The packages installed in the tutorial |

## Requirements

- Python 3 (the CI workflow uses 3.12)
- `paho-mqtt>=2,<3` and `pytest`
- Docker (for the Eclipse Mosquitto test broker)

## Run it on the free public broker

1. Install the packages:

   ```bash
   pip install "paho-mqtt>=2,<3" pytest
   ```

2. Start a throwaway Mosquitto broker for the integration tests:

   ```bash
   docker run -d --name test-broker -p 1883:1883 eclipse-mosquitto:2 \
     mosquitto -c /mosquitto-no-auth.conf
   ```

3. Run the unit and integration tests:

   ```bash
   pytest -q
   ```

   To test reconnect logic, restart the container mid-test with `docker restart test-broker`.

4. Run the end-to-end smoke test against `broker.connectmq.com` (anonymous TLS on port 8883):

   ```bash
   python smoke_test.py
   ```

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-testing-mqtt-clients-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-testing-mqtt-clients-private) — the **Free** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. `smoke_test.py` already reads its settings from the environment and always uses TLS on port 8883. Create a dedicated credential set for CI (not a device's identity) and set these variables, for example from CI secrets:

   ```bash
   export MQTT_HOST=YOUR_BROKER_HOST
   export MQTT_USERNAME=YOUR_USERNAME
   export MQTT_PASSWORD=YOUR_PASSWORD
   export MQTT_CLIENT_ID=YOUR_CLIENT_ID
   export MQTT_PREFIX=YOUR_TOPIC_PREFIX
   python smoke_test.py
   ```

   `adapter.build_client()` also accepts `username=`, `password=` and `tls=True` for a private broker on port 8883.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [Testing MQTT Clients: Unit, Integration and End-to-End Tests](https://connectmq.com/blog/testing-mqtt-clients/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-testing-mqtt-clients-related) — the full tutorial with explanations
- 🧩 [Python basic example](../../python/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-testing-mqtt-clients-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-testing-mqtt-clients-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-testing-mqtt-clients-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-testing-mqtt-clients-footer">Blog</a>
</p>
