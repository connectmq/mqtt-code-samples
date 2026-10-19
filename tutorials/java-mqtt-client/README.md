# Java MQTT Client Tutorial: Eclipse Paho vs HiveMQ Client with TLS and MQTT 5

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-java-mqtt-client-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-java-mqtt-client-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Compare the two main Java MQTT libraries, Eclipse Paho and the HiveMQ MQTT Client, and implement publish/subscribe over TLS with MQTT 5 using each of them.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-java-mqtt-client-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-java-mqtt-client-intro)

📖 **Full step-by-step tutorial:** [Java MQTT Client Tutorial: Eclipse Paho vs HiveMQ Client with TLS and MQTT 5](https://connectmq.com/blog/java-mqtt-client/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-java-mqtt-client-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-java-mqtt-client-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`PahoDemo.java`](PahoDemo.java) | Eclipse Paho MQTT 5 client: TLS on 8883, automatic reconnect, persistent session, retained Last Will, subscribes to `<prefix>/cmd/#` and publishes JSON telemetry every 5 s |
| [`HiveMqDemo.java`](HiveMqDemo.java) | The same program with the HiveMQ MQTT Client's fluent async API, plus MQTT 5 `contentType` and `messageExpiryInterval` properties |

## Requirements

- Java 17 and Maven
- [Eclipse Paho](https://eclipse.dev/paho/) `org.eclipse.paho.mqttv5.client` 1.2.5 and/or HiveMQ `hivemq-mqtt-client` 1.3.3
- No keystore setup: the JDK trust store already includes ISRG Root X1 (Let's Encrypt) used by the broker
- Optionally, `mosquitto_sub` / `mosquitto_pub` for testing

## Run it on the free public broker

1. Create a Maven project (Java 17) and add one or both dependencies to `pom.xml`:

   ```xml
   <dependencies>
     <dependency>
       <groupId>org.eclipse.paho</groupId>
       <artifactId>org.eclipse.paho.mqttv5.client</artifactId>
       <version>1.2.5</version>
     </dependency>
     <dependency>
       <groupId>com.hivemq</groupId>
       <artifactId>hivemq-mqtt-client</artifactId>
       <version>1.3.3</version>
     </dependency>
   </dependencies>
   ```

2. Copy `PahoDemo.java` and/or `HiveMqDemo.java` into `src/main/java` and run either class. By default both connect to `broker.connectmq.com:8883` with TLS and use the prefix `connectmq/demo/j6t1ve` — change it to your own random prefix (environment variable `MQTT_PREFIX`).
3. Watch the topics and send a command from a terminal:

   ```bash
   mosquitto_sub -h broker.connectmq.com -p 1883 -i watch-j6t1ve -t 'connectmq/demo/j6t1ve/#' -v
   mosquitto_pub -h broker.connectmq.com -p 1883 -i send-j6t1ve -t 'connectmq/demo/j6t1ve/cmd/valve' -m 'close'
   ```

Run only one client at a time with the default IDs, or give each its own ID (`MQTT_CLIENT_ID`); two clients cannot share a session.

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-java-mqtt-client-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-java-mqtt-client-private) — the **Serverless (Free)** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. Both classes read their settings from environment variables, so no code changes are needed. Use the generated credentials (the client ID is bound to them and must match exactly):

   ```bash
   export MQTT_CLIENT_ID=YOUR_CLIENT_ID
   export MQTT_USERNAME=YOUR_USERNAME
   export MQTT_PASSWORD=YOUR_PASSWORD
   export MQTT_PREFIX=warehouse/zone3/gateway
   ```

   `PahoDemo` reads the full URI from `MQTT_URL` (`ssl://YOUR_BROKER_HOST:8883`); `HiveMqDemo` reads the host from `MQTT_HOST` and always uses port 8883 with TLS.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [Java MQTT Client Tutorial: Eclipse Paho vs HiveMQ Client with TLS and MQTT 5](https://connectmq.com/blog/java-mqtt-client/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-java-mqtt-client-related) — the full tutorial with explanations
- 🧩 [Java basic example](../../java/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-java-mqtt-client-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-java-mqtt-client-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-java-mqtt-client-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-java-mqtt-client-footer">Blog</a>
</p>
