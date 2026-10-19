# Python MQTT TLS: Connecting Securely on Port 8883 with paho-mqtt

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-python-mqtt-tls-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-python-mqtt-tls-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Encrypt your Python MQTT traffic with paho-mqtt and TLS on port 8883: use the system CA store, keep hostname verification on, fix the common certificate errors, and connect over secure WebSocket when only 443-style ports are open.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-python-mqtt-tls-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-python-mqtt-tls-intro)

📖 **Full step-by-step tutorial:** [Python MQTT TLS: Connecting Securely on Port 8883 with paho-mqtt](https://connectmq.com/blog/python-mqtt-tls/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-python-mqtt-tls-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-python-mqtt-tls-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`tls_client.py`](tls_client.py) | Connects on port 8883 with the system CA store and hostname verification, prints the TLS version and cipher, then publishes and receives a test message |
| [`requirements.txt`](requirements.txt) | Python dependency (`paho-mqtt>=2.0`) |

## Requirements

- Python 3 (a virtual environment is recommended)
- [paho-mqtt](https://pypi.org/project/paho-mqtt/) 2.0 or newer
- An up-to-date CA store on your machine (the broker uses a Let's Encrypt certificate; no custom CA file needed)
- Optional: `openssl` to check the certificate chain

## Run it on the free public broker

1. Create a virtual environment and install paho-mqtt:

   ```bash
   python -m venv .venv
   source .venv/bin/activate          # Windows: .venv\Scripts\activate
   pip install "paho-mqtt>=2.0"
   ```

2. Check that the broker's certificate validates from your machine (look for `Verification: OK`):

   ```bash
   openssl s_client -connect broker.connectmq.com:8883 -servername broker.connectmq.com -brief </dev/null
   ```

3. Replace `k7f3q2` in `TOPIC` with your own random string and run the client:

   ```bash
   python tls_client.py
   ```

   You should see something like `Connected over TLSv1.3 using TLS_AES_256_GCM_SHA384`, followed by your message coming back.

Prefer full control over the SSL context? Replace the `tls_set(...)` call with:

```python
context = ssl.create_default_context()
context.minimum_version = ssl.TLSVersion.TLSv1_2
client.tls_set_context(context)
```

Only web ports open? Tunnel MQTT through secure WebSocket on port 8084 with the same TLS verification:

```python
client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id=f"wss-{uuid.uuid4().hex[:8]}",
    transport="websockets",
)
client.ws_set_options(path="/mqtt")
client.tls_set()
client.connect("broker.connectmq.com", 8084, keepalive=60)
```

Getting `CERTIFICATE_VERIFY_FAILED` on macOS with Python from python.org? Run "Install Certificates.command", or `pip install certifi` and call `client.tls_set(ca_certs=certifi.where())`. Never "fix" TLS with `tls_insecure_set(True)` or `cert_reqs=ssl.CERT_NONE`.

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-python-mqtt-tls-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-python-mqtt-tls-private) — the **Serverless (Free)** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. `tls_client.py` already uses TLS on port 8883. Set `BROKER` to your broker host, use the client ID shown in the portal, and add credentials before `client.connect(...)` — as in the post:

   ```python
   client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="YOUR_CLIENT_ID")
   client.username_pw_set("YOUR_USERNAME", "YOUR_PASSWORD")
   client.tls_set()
   client.connect("broker.connectmq.com", 8883, keepalive=60)
   ```

   Load secrets from environment variables (`os.environ["MQTT_PASSWORD"]`) rather than committing them to source control.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [Python MQTT TLS: Connecting Securely on Port 8883 with paho-mqtt](https://connectmq.com/blog/python-mqtt-tls/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-python-mqtt-tls-related) — the full tutorial with explanations
- 🧩 [Python basic example](../../python/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-python-mqtt-tls-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-python-mqtt-tls-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-python-mqtt-tls-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-python-mqtt-tls-footer">Blog</a>
</p>
