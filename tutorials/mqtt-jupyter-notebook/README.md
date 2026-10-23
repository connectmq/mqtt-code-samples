# Exploring MQTT Data in a Jupyter Notebook: Subscribe, Plot and Save Snapshots

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-jupyter-notebook-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-jupyter-notebook-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

A cell-by-cell guide to exploring MQTT data in Jupyter: connect paho-mqtt in the background, inspect raw payloads, plot live charts, save snapshots and avoid the duplicate-client trap when re-running cells.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-jupyter-notebook-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-jupyter-notebook-intro)

📖 **Full step-by-step tutorial:** [Exploring MQTT Data in a Jupyter Notebook: Subscribe, Plot and Save Snapshots](https://connectmq.com/blog/mqtt-jupyter-notebook/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-jupyter-notebook-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-jupyter-notebook-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`mqtt_exploration.ipynb`](mqtt_exploration.ipynb) | The post's cells in order: config, background subscriber, demo publisher, raw inspection, DataFrame, live plot, Parquet snapshots, clean-up |
| [`requirements.txt`](requirements.txt) | Packages the post installs (`paho-mqtt>=2.0`, pandas, matplotlib, pyarrow) |

## Requirements

- Python 3.9 or newer
- A Jupyter environment: JupyterLab, the classic notebook interface or VS Code's notebook editor
- `paho-mqtt>=2.0`, `pandas`, `matplotlib`
- `pyarrow` (only for Parquet snapshots)

## Run it on the free public broker

1. Open `mqtt_exploration.ipynb` in Jupyter and run the setup cell so the packages land in the kernel's environment:

   ```python
   %pip install "paho-mqtt>=2.0" pandas matplotlib pyarrow
   ```

2. Run Cell 1 (configuration, prints a random topic prefix) and Cell 2 (connects the subscriber in a background thread with `loop_start()`).
3. Run Cell 3 to start the demo publisher (three simulated temperature sensors for two minutes), or set `PREFIX` to an existing stream and skip it.
4. Run Cells 4–7 to inspect raw messages, build a DataFrame, plot a live chart and save Parquet snapshots.
5. Run Cell 8 to stop the loop and disconnect before closing the notebook.

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-jupyter-notebook-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-jupyter-notebook-private) — the **Free** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. Only the connection lines in Cell 2 change: call `sub.username_pw_set("YOUR_USERNAME", "YOUR_PASSWORD")`, call `sub.tls_set()`, use `client_id="YOUR_CLIENT_ID"` and connect to port 8883 (set `BROKER` to your broker host and `PORT = 8883` in Cell 1). The broker's Let's Encrypt certificate is trusted by the default system store.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [Exploring MQTT Data in a Jupyter Notebook: Subscribe, Plot and Save Snapshots](https://connectmq.com/blog/mqtt-jupyter-notebook/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-jupyter-notebook-related) — the full tutorial with explanations
- 🧩 [Python basic example](../../python/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-jupyter-notebook-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-jupyter-notebook-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-jupyter-notebook-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-jupyter-notebook-footer">Blog</a>
</p>
