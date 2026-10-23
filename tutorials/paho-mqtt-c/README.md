# Paho MQTT C Client Tutorial for Embedded Linux

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-c-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-c-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

A practical Paho MQTT C tutorial for embedded Linux: build the library with OpenSSL, write a TLS publisher and subscriber, cross-compile for ARM, and run it reliably under systemd.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-c-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-c-intro)

📖 **Full step-by-step tutorial:** [Paho MQTT C Client Tutorial for Embedded Linux](https://connectmq.com/blog/paho-mqtt-c/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-c-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-c-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`publisher.c`](publisher.c) | Synchronous Paho C publisher over TLS (8883) with hostname verification, env-var credentials, reconnect with backoff and a JSON reading every 5 s |
| [`subscriber.c`](subscriber.c) | Subscriber to `<prefix>/+/temperature`: the publisher's helpers plus the post's subscriber `main`, which reconnects and resubscribes |
| [`mqtt-publisher.service`](mqtt-publisher.service) | systemd unit that runs the publisher with credentials from environment variables and restarts it on failure |

## Requirements

- Embedded Linux or any Linux (Debian, Ubuntu, Raspberry Pi OS, Yocto, Buildroot)
- GCC and the [Eclipse Paho MQTT C](https://github.com/eclipse-paho/paho.mqtt.c) library built with OpenSSL (`paho-mqtt3cs`)
- OpenSSL development headers and a CA bundle (`ca-certificates`, `/etc/ssl/certs/ca-certificates.crt`)
- Optional: CMake and an ARM cross toolchain (`aarch64-linux-gnu-gcc`) for cross-compiling, `mosquitto_sub` to watch messages

## Run it on the free public broker

1. Install the library from packages:

   ```bash
   sudo apt update
   sudo apt install -y build-essential libpaho-mqtt-dev libssl-dev ca-certificates
   ```

   or build the latest release from source:

   ```bash
   git clone https://github.com/eclipse-paho/paho.mqtt.c.git
   cd paho.mqtt.c
   cmake -B build -DPAHO_WITH_SSL=TRUE -DPAHO_BUILD_SAMPLES=FALSE -DPAHO_BUILD_STATIC=FALSE -DCMAKE_BUILD_TYPE=Release
   cmake --build build -j"$(nproc)"
   sudo cmake --install build
   sudo ldconfig
   ```

2. Build and run the publisher (it connects anonymously to `ssl://broker.connectmq.com:8883`; set `MQTT_TOPIC_PREFIX` to your own prefix, default `connectmq/demo/paho-c-4821`):

   ```bash
   gcc -Wall -O2 -o publisher publisher.c -lpaho-mqtt3cs
   ./publisher
   ```

3. Build and run the subscriber the same way (`gcc -Wall -O2 -o subscriber subscriber.c -lpaho-mqtt3cs`), or watch the publisher with no code at all:

   ```bash
   mosquitto_sub -h broker.connectmq.com -p 1883 -i watcher-4821 -t "connectmq/demo/paho-c-4821/#" -v
   ```

4. Cross-compile for an ARM board:

   ```bash
   cmake -B build-arm \
     -DCMAKE_C_COMPILER=aarch64-linux-gnu-gcc \
     -DCMAKE_SYSTEM_NAME=Linux \
     -DPAHO_WITH_SSL=TRUE \
     -DOPENSSL_ROOT_DIR=/opt/sysroot/usr \
     -DPAHO_BUILD_SHARED=TRUE -DPAHO_BUILD_SAMPLES=FALSE \
     -DCMAKE_INSTALL_PREFIX=/opt/paho-arm -DCMAKE_INSTALL_LIBDIR=lib
   cmake --build build-arm -j"$(nproc)"
   cmake --install build-arm

   aarch64-linux-gnu-gcc -O2 -o publisher publisher.c \
     -I/opt/paho-arm/include -L/opt/paho-arm/lib -lpaho-mqtt3cs -lssl -lcrypto -lpthread

   # Copy the binary and the shared library to the board
   scp publisher /opt/paho-arm/lib/libpaho-mqtt3cs.so* root@gateway:/usr/local/lib/
   ```

   On the board, move `publisher` to `/usr/local/bin` and run `ldconfig`. Make sure the image contains a CA bundle and a correct clock.

If TLS connect fails or hangs, test the port with `openssl s_client -connect broker.connectmq.com:8883`.

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-c-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-c-private) — the **Free** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. In `publisher.c` (and `subscriber.c`), change `ADDRESS` to `"ssl://YOUR_BROKER_HOST:8883"`. Credentials and client ID come from environment variables, so fill them into `mqtt-publisher.service` and install it:

   ```text
   Environment=MQTT_CLIENT_ID=YOUR_CLIENT_ID
   Environment=MQTT_USERNAME=YOUR_USERNAME
   Environment=MQTT_PASSWORD=YOUR_PASSWORD
   ```

   ```bash
   sudo cp mqtt-publisher.service /etc/systemd/system/
   sudo systemctl daemon-reload
   sudo systemctl enable --now mqtt-publisher
   journalctl -u mqtt-publisher -f
   ```

   Client IDs are bound to their credentials, so give each gateway its own set. The subscriber uses the fixed client ID `paho-c-sub-4821`; change it to its own issued client ID.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [Paho MQTT C Client Tutorial for Embedded Linux](https://connectmq.com/blog/paho-mqtt-c/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-c-related) — the full tutorial with explanations
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-c-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-c-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-c-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-paho-mqtt-c-footer">Blog</a>
</p>
