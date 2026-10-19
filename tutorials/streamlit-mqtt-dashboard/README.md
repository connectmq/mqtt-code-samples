# Streamlit MQTT Dashboard in Pure Python: Live Sensor Charts in 100 Lines

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-streamlit-mqtt-dashboard-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-streamlit-mqtt-dashboard-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Build a live Streamlit dashboard fed by a background paho-mqtt subscriber connected to broker.connectmq.com, with a thread-safe buffer, auto-refreshing charts and a simulator to feed it.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-streamlit-mqtt-dashboard-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-streamlit-mqtt-dashboard-intro)

📖 **Full step-by-step tutorial:** [Streamlit MQTT Dashboard in Pure Python: Live Sensor Charts in 100 Lines](https://connectmq.com/blog/streamlit-mqtt-dashboard/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-streamlit-mqtt-dashboard-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-streamlit-mqtt-dashboard-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`simulator.py`](simulator.py) | Publishes simulated temperature and humidity readings for three sensors every second |
| [`dashboard.py`](dashboard.py) | Streamlit app with a cached background paho-mqtt subscriber, thread-safe buffer and auto-refreshing charts |
| [`requirements.txt`](requirements.txt) | The packages installed in the tutorial |

## Requirements

- Python 3.9 or newer
- `streamlit>=1.37` (for `st.fragment(run_every=...)`)
- `paho-mqtt>=2.0`
- `pandas`

## Run it on the free public broker

1. Create a virtual environment and install the packages:

   ```bash
   python -m venv .venv
   source .venv/bin/activate        # Windows: .venv\Scripts\activate
   pip install "streamlit>=1.37" "paho-mqtt>=2.0" pandas
   ```

2. Replace `k7f3q2` in `PREFIX` with your own random string in **both** `simulator.py` and `dashboard.py`.
3. Start the simulator in its own terminal and leave it running:

   ```bash
   python simulator.py
   ```

4. Start the dashboard and open `http://localhost:8501`:

   ```bash
   streamlit run dashboard.py
   ```

5. If the dashboard stays on "Connecting...", test the broker from the command line:

   ```bash
   mosquitto_sub -h broker.connectmq.com -p 1883 -i test-k7f3q2 -t 'connectmq/demo/k7f3q2/#' -v
   ```

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-streamlit-mqtt-dashboard-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-streamlit-mqtt-dashboard-private) — the **Serverless (Free)** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. In `dashboard.py`, set `BROKER` to your broker host and `PORT = 8883`, then uncomment the private-broker lines that are already in `start_mqtt()`:

   ```python
   # For a private ConnectMQ broker:
   client.username_pw_set("YOUR_USERNAME", "YOUR_PASSWORD")
   client.tls_set()  # and use port 8883
   ```

   Do the same in `simulator.py` (`BROKER`, port `8883` in `client.connect(...)`, `username_pw_set` and `tls_set()` before connecting). The post recommends keeping secrets in `.streamlit/secrets.toml` and reading them with `st.secrets["mqtt"]["username"]` instead of hard-coding them.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [Streamlit MQTT Dashboard in Pure Python: Live Sensor Charts in 100 Lines](https://connectmq.com/blog/streamlit-mqtt-dashboard/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-streamlit-mqtt-dashboard-related) — the full tutorial with explanations
- 🧩 [Python basic example](../../python/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-streamlit-mqtt-dashboard-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-streamlit-mqtt-dashboard-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-streamlit-mqtt-dashboard-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-streamlit-mqtt-dashboard-footer">Blog</a>
</p>
