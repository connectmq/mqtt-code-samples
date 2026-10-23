# Paho MQTT Reconnect: Robust Backoff, Resubscribe and Offline Buffering in Python

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-reconnect-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-reconnect-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Why paho-mqtt clients silently stop receiving or lose messages after a network drop, and a tested Python client that adds backoff with jitter, resubscription, an offline queue and persistent MQTT 5 sessions.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-reconnect-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-reconnect-intro)

📖 **Full step-by-step tutorial:** [Paho MQTT Reconnect: Robust Backoff, Resubscribe and Offline Buffering in Python](https://connectmq.com/blog/paho-mqtt-reconnect/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-reconnect-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-reconnect-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`resilient_client.py`](resilient_client.py) | `ResilientClient` with `connect_async()`, jittered exponential backoff, resubscribe in `on_connect`, a bounded offline buffer and an MQTT 5 persistent session, plus a demo that publishes telemetry every 2 s and logs commands |
| [`requirements.txt`](requirements.txt) | Python dependency (`paho-mqtt>=2.0`) |

## Requirements

- Python 3
- [paho-mqtt](https://pypi.org/project/paho-mqtt/) 2.x
- Optional: `mosquitto_sub` / `mosquitto_pub` and (on Linux) `iptables` to test failure modes

## Run it on the free public broker

1. Install paho-mqtt and start the client:

   ```bash
   pip install "paho-mqtt>=2.0"
   python resilient_client.py
   ```

   It prints the generated topic prefix (`connectmq/demo/<run-id>`), publishes to `<prefix>/telemetry` and logs commands sent to `<prefix>/cmd/...`.

2. Watch it from a second terminal (replace `<run-id>` with the printed value):

   ```bash
   mosquitto_sub -h broker.connectmq.com -p 1883 -i watch-<run-id> -t "connectmq/demo/<run-id>/#" -v
   ```

3. Break it on purpose:
   - **Network drop:** disable Wi-Fi for 30 seconds; the log shows "connection lost", growing delays, then "connected" and "flushing N buffered messages".
   - **Blocked port on Linux:**

     ```bash
     sudo iptables -A OUTPUT -p tcp --dport 1883 -j DROP
     # wait 60 seconds, then remove the rule
     sudo iptables -D OUTPUT -p tcp --dport 1883 -j DROP
     ```

   - **Start offline:** disconnect the network before starting; `connect_async()` waits and connects when the network returns.
   - **Session takeover:** start a second client with the same ID, for example `mosquitto_sub -i resilient-<run-id> -t x`.
   - **Commands during an outage:** publish a QoS 1 command to `<prefix>/cmd/...` while the client is offline; the kept session delivers it when the client returns.

On the public broker sessions expire after at most 30 minutes, so the 1,800-second session expiry is the maximum useful value there.

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-reconnect-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-reconnect-private) — the **Free** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. In the `__main__` block of `resilient_client.py`, construct the client with TLS on port 8883 and your issued credentials (use your broker's host name from the portal):

   ```python
   rc = ResilientClient(
       host="broker.connectmq.com", port=8883, use_tls=True,
       client_id="YOUR_CLIENT_ID", username="YOUR_USERNAME", password="YOUR_PASSWORD",
       subscriptions=[("connectmq/factory1/production/line1/+/cmd", 1)],
   )
   ```

   Keep the client ID stable: the persistent session is tied to it. Stop retrying on reason codes 0x86 (bad credentials) and 0x87 (not authorized), because brokers, ConnectMQ included, block an IP after repeated failed logins.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [Paho MQTT Reconnect: Robust Backoff, Resubscribe and Offline Buffering in Python](https://connectmq.com/blog/paho-mqtt-reconnect/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-reconnect-related) — the full tutorial with explanations
- 🧩 [Python basic example](../../python/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-reconnect-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-reconnect-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-reconnect-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-reconnect-footer">Blog</a>
</p>
