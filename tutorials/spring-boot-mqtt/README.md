# Spring Boot MQTT Integration: Consume Device Data and Expose It via REST

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-spring-boot-mqtt-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-spring-boot-mqtt-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Use Spring Integration's MQTT 5 adapters in Spring Boot to consume device telemetry over TLS, keep the latest readings in memory, expose them through REST and send commands back to devices.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-spring-boot-mqtt-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-spring-boot-mqtt-intro)

📖 **Full step-by-step tutorial:** [Spring Boot MQTT Integration: Consume Device Data and Expose It via REST](https://connectmq.com/blog/spring-boot-mqtt/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-spring-boot-mqtt-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-spring-boot-mqtt-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`src/main/resources/application.yml`](src/main/resources/application.yml) | Broker URL (`ssl://broker.connectmq.com:8883`), client ID, credentials and topic prefix, overridable by environment variables |
| [`src/main/java/com/example/mqttdemo/MqttConfig.java`](src/main/java/com/example/mqttdemo/MqttConfig.java) | One shared `Mqttv5ClientManager`, the inbound telemetry adapter and flow, and the outbound handler |
| [`src/main/java/com/example/mqttdemo/MqttGateway.java`](src/main/java/com/example/mqttdemo/MqttGateway.java) | Messaging gateway interface for publishing to any topic |
| [`src/main/java/com/example/mqttdemo/ReadingStore.java`](src/main/java/com/example/mqttdemo/ReadingStore.java) | Keeps the latest JSON reading per device in a `ConcurrentHashMap` |
| [`src/main/java/com/example/mqttdemo/DeviceController.java`](src/main/java/com/example/mqttdemo/DeviceController.java) | REST API: `GET /api/devices`, `GET /api/devices/{id}`, `POST /api/devices/{id}/commands` |

Add these files to a Spring Boot 3 project (package `com.example.mqttdemo`, with the usual `@SpringBootApplication` class) and add the dependencies below to its `pom.xml`:

```xml
<parent>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-parent</artifactId>
  <version>3.3.5</version>
</parent>

<dependencies>
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-web</artifactId>
  </dependency>
  <dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-integration</artifactId>
  </dependency>
  <dependency>
    <groupId>org.springframework.integration</groupId>
    <artifactId>spring-integration-mqtt</artifactId>
  </dependency>
  <dependency>
    <groupId>org.eclipse.paho</groupId>
    <artifactId>org.eclipse.paho.mqttv5.client</artifactId>
    <version>1.2.5</version>
  </dependency>
</dependencies>
```

The Paho MQTT 5 client is an optional dependency of `spring-integration-mqtt`; without it you get `ClassNotFoundException: org.eclipse.paho.mqttv5...` at startup.

## Requirements

- Java 17+
- Spring Boot 3 (3.3.5 in the post) with Spring Integration 6 (`spring-integration-mqtt`)
- Eclipse Paho MQTT 5 client `org.eclipse.paho.mqttv5.client` 1.2.5
- Maven (`./mvnw`), `mosquitto_pub` / `mosquitto_sub` and `curl` for testing

## Run it on the free public broker

The defaults in `application.yml` already point at `ssl://broker.connectmq.com:8883` (TLS, trusted by the JDK out of the box). Use your own random prefix via `MQTT_PREFIX` and only test data.

1. Start the application:

   ```bash
   ./mvnw spring-boot:run
   ```

2. Simulate a device:

   ```bash
   mosquitto_pub -h broker.connectmq.com -p 1883 -i dev-s8d2lf \
     -t 'connectmq/demo/s8d2lf/devices/sensor-1/telemetry' -m '{"temperature":22.5,"humidity":48}'
   ```

3. Query the REST API:

   ```bash
   curl -s http://localhost:8080/api/devices
   curl -s http://localhost:8080/api/devices/sensor-1
   ```

4. Send a command and watch it arrive on the device topic:

   ```bash
   mosquitto_sub -h broker.connectmq.com -p 1883 -i cmdwatch-s8d2lf \
     -t 'connectmq/demo/s8d2lf/devices/+/cmd' -v &
   curl -s -X POST http://localhost:8080/api/devices/sensor-1/commands \
     -H 'Content-Type: application/json' -d '{"fan":"on"}'
   ```

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-spring-boot-mqtt-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-spring-boot-mqtt-private) — the **Free** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. No code change is needed: `application.yml` reads everything from the environment, and `MqttConfig` sets the username and password when `MQTT_USERNAME` is not blank. Set the generated values (the client ID must match exactly):

   ```bash
   export MQTT_URL=ssl://YOUR_BROKER_HOST:8883
   export MQTT_CLIENT_ID=YOUR_CLIENT_ID
   export MQTT_USERNAME=YOUR_USERNAME
   export MQTT_PASSWORD=YOUR_PASSWORD
   export MQTT_PREFIX=YOUR_TOPIC_PREFIX
   ./mvnw spring-boot:run
   ```

   Inbound and outbound share one `Mqttv5ClientManager`, so the service uses exactly one connection per client ID. Each replica needs its own credentials.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [Spring Boot MQTT Integration: Consume Device Data and Expose It via REST](https://connectmq.com/blog/spring-boot-mqtt/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-spring-boot-mqtt-related) — the full tutorial with explanations
- 🧩 [Java basic example](../../java/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-spring-boot-mqtt-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-spring-boot-mqtt-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-spring-boot-mqtt-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-spring-boot-mqtt-footer">Blog</a>
</p>
