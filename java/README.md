# Java MQTT Example

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=java-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=java-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../LICENSE)

Connect Java to an MQTT broker with the Eclipse Paho Java client. Start on the free public broker, then point the same code at a secure private broker on ConnectMQ.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=java-intro)** — the managed, serverless MQTT broker for IoT. Try this example on the free public broker in seconds, then move the very same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=java-intro)

Full walkthrough on the website: **[Java MQTT example](https://connectmq.com/code-samples/java/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=java-intro)**

## Requirements

- **Library:** [Eclipse Paho Java Client](https://github.com/eclipse/paho.mqtt.java)
- **Install:**

```bash
<!-- Maven -->
<dependency>
  <groupId>org.eclipse.paho</groupId>
  <artifactId>org.eclipse.paho.client.mqttv3</artifactId>
  <version>1.2.5</version>
</dependency>
```

## Files

| Folder | Broker | What it does |
| --- | --- | --- |
| [`public-broker/`](public-broker/) | Free public broker `broker.connectmq.com` | Connect without an account, subscribe and publish a JSON reading |
| [`private-broker/`](private-broker/) | Your private ConnectMQ broker | The same flow over TLS with your username and password |

## How to run

1. Add the Eclipse Paho dependency (`org.eclipse.paho:org.eclipse.paho.client.mqttv3:1.2.5`) to your Maven or Gradle project.
2. Put `Example.java` in your sources and run the `Example` class.

---

## 1. Try it on the free public broker (no account needed)

No account needed: connect to broker.connectmq.com on port 1883 and start publishing in seconds.

| Protocol | URL |
| --- | --- |
| MQTT (TCP) | `mqtt://broker.connectmq.com:1883` |
| MQTT over TLS | `mqtts://broker.connectmq.com:8883` |
| WebSocket | `ws://broker.connectmq.com:8083/mqtt` |
| Secure WebSocket | `wss://broker.connectmq.com:8084/mqtt` |

**`Example.java`** ([open file](public-broker/Example.java))

```java
import org.eclipse.paho.client.mqttv3.*;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;

public class Example {
    public static void main(String[] args) throws Exception {
        String topic = "your-project/sensors/temperature"; // Use a unique topic prefix: everyone can read the public broker

        // Connect to the free public broker (no account needed)
        MqttClient client = new MqttClient("tcp://broker.connectmq.com:1883",
                MqttClient.generateClientId(), new MemoryPersistence());
        MqttConnectOptions options = new MqttConnectOptions();
        // Reconnect automatically if the connection drops
        options.setAutomaticReconnect(true);
        client.connect(options);

        // Subscribe to the temperature topic
        client.subscribe(topic, 1, (t, message) ->
                System.out.println(t + ": " + new String(message.getPayload())));

        // Publish a JSON reading
        client.publish(topic, "{\"temperature\":21.5}".getBytes(), 1, false);
    }
}
```

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic, including yours. Never send passwords, personal data or anything confidential through it, and use a unique topic prefix (`your-project/...`) so your messages don't mix with others'. There is no guarantee of availability or message retention. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=java-public)

## 2. Go to production with a private ConnectMQ broker

For real devices, use a private serverless MQTT broker on ConnectMQ instead of the public one: TLS encryption, a username and password for every device and per-topic access control, fully managed. The Serverless (Free) plan needs no credit card.

**Get your private broker in under a minute:**

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=java-private) — no credit card.
2. Create a broker in the dashboard (the **Serverless (Free)** plan is enough to start).
3. Copy the **host**, **username** and **password** of your broker.
4. Replace `YOUR_BROKER_HOST`, `YOUR_USERNAME` and `YOUR_PASSWORD` in the files under [`private-broker/`](private-broker/) and run them.

**`Example.java`** ([open file](private-broker/Example.java))

```java
import org.eclipse.paho.client.mqttv3.*;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;

public class Example {
    public static void main(String[] args) throws Exception {
        String topic = "your-project/sensors/temperature";

        // Connect to your private ConnectMQ broker on port 8883 (TLS: the system CA store verifies the broker certificate)
        MqttClient client = new MqttClient("ssl://YOUR_BROKER_HOST:8883",
                MqttClient.generateClientId(), new MemoryPersistence());
        MqttConnectOptions options = new MqttConnectOptions();
        // Username and password from your ConnectMQ dashboard
        options.setUserName("YOUR_USERNAME");
        options.setPassword("YOUR_PASSWORD".toCharArray());
        // Reconnect automatically if the connection drops
        options.setAutomaticReconnect(true);
        client.connect(options);

        // Subscribe to the temperature topic
        client.subscribe(topic, 1, (t, message) ->
                System.out.println(t + ": " + new String(message.getPayload())));

        // Publish a JSON reading
        client.publish(topic, "{\"temperature\":21.5}".getBytes(), 1, false);
    }
}
```

### What you get with a private broker

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Devices & connections dashboard** — live device status, last values, connection history
- ⚡ **Fully managed and serverless** — no servers to patch or scale

## Public vs. private broker

| | Free public broker | Private broker on ConnectMQ |
| --- | --- | --- |
| Account | Not needed | Free sign-up, no credit card |
| Host | `broker.connectmq.com` | Your own broker host |
| Who can read your topics | **Anyone** | Only your devices |
| Encryption | Optional (TLS on 8883) | TLS on every connection |
| Authentication | None | Username and password per device |
| Topic access control (ACL) | No | Yes, per topic and per client |
| Device & connection dashboard | No | Yes |
| Use it for | Learning, demos, quick tests | Real devices and production |

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=java-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=java-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=java-footer">Pricing</a> ·
  <a href="https://connectmq.com/code-samples/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=java-footer">All code samples</a>
</p>
