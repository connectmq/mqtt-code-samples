# Rust MQTT Example

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=rust-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=rust-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../LICENSE)

Connect Rust to an MQTT broker with the rumqttc crate. Start on the free public broker, then point the same code at a secure private broker on ConnectMQ.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=rust-intro)** — the managed, serverless MQTT broker for IoT. Try this example on the free public broker in seconds, then move the very same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=rust-intro)

Full walkthrough on the website: **[Rust MQTT example](https://connectmq.com/code-samples/rust/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=rust-intro)**

## Requirements

- **Library:** [rumqttc](https://crates.io/crates/rumqttc)
- **Install:**

```bash
cargo add rumqttc
```

## Files

| Folder | Broker | What it does |
| --- | --- | --- |
| [`public-broker/`](public-broker/) | Free public broker `broker.connectmq.com` | Connect without an account, subscribe and publish a JSON reading |
| [`private-broker/`](private-broker/) | Your private ConnectMQ broker | The same flow over TLS with your username and password |

## How to run

```bash
cd public-broker   # or private-broker
cargo new mqtt-example && cd mqtt-example
cargo add rumqttc
# replace src/main.rs with this folder's main.rs
cargo run
```

---

## 1. Try it on the free public broker (no account needed)

No account needed: connect to broker.connectmq.com on port 1883 and start publishing in seconds.

| Protocol | URL |
| --- | --- |
| MQTT (TCP) | `mqtt://broker.connectmq.com:1883` |
| MQTT over TLS | `mqtts://broker.connectmq.com:8883` |
| WebSocket | `ws://broker.connectmq.com:8083/mqtt` |
| Secure WebSocket | `wss://broker.connectmq.com:8084/mqtt` |

**`main.rs`** ([open file](public-broker/main.rs))

```rust
use rumqttc::{Client, Event, MqttOptions, Packet, QoS};
use std::time::Duration;

fn main() {
    let topic = "your-project/sensors/temperature"; // Use a unique topic prefix: everyone can read the public broker

    // Connect to the free public broker (no account needed) (Every client needs a unique client ID)
    let mut options = MqttOptions::new("rust-example", "broker.connectmq.com", 1883);
    options.set_keep_alive(Duration::from_secs(30));
    let (client, mut connection) = Client::new(options, 10);

    // Subscribe to the temperature topic
    client.subscribe(topic, QoS::AtLeastOnce).unwrap();
    // Publish a JSON reading
    client.publish(topic, QoS::AtLeastOnce, false, r#"{"temperature":21.5}"#).unwrap();

    // Keep the client running
    for event in connection.iter() {
        if let Ok(Event::Incoming(Packet::Publish(p))) = event {
            println!("{}: {}", p.topic, String::from_utf8_lossy(&p.payload));
        }
    }
}
```

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic, including yours. Never send passwords, personal data or anything confidential through it, and use a unique topic prefix (`your-project/...`) so your messages don't mix with others'. There is no guarantee of availability or message retention. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=rust-public)

## 2. Go to production with a private ConnectMQ broker

For real devices, use a private serverless MQTT broker on ConnectMQ instead of the public one: TLS encryption, a username and password for every device and per-topic access control, fully managed. The Serverless (Free) plan needs no credit card.

**Get your private broker in under a minute:**

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=rust-private) — no credit card.
2. Create a broker in the dashboard (the **Serverless (Free)** plan is enough to start).
3. Copy the **host**, **username** and **password** of your broker.
4. Replace `YOUR_BROKER_HOST`, `YOUR_USERNAME` and `YOUR_PASSWORD` in the files under [`private-broker/`](private-broker/) and run them.

**`main.rs`** ([open file](private-broker/main.rs))

```rust
use rumqttc::{Client, Event, MqttOptions, Packet, QoS, Transport};
use std::time::Duration;

fn main() {
    let topic = "your-project/sensors/temperature";

    // Connect to your private ConnectMQ broker on port 8883 (Every client needs a unique client ID)
    let mut options = MqttOptions::new("rust-example", "YOUR_BROKER_HOST", 8883);
    options.set_keep_alive(Duration::from_secs(30));
    // Username and password from your ConnectMQ dashboard
    options.set_credentials("YOUR_USERNAME", "YOUR_PASSWORD");
    // TLS: the system CA store verifies the broker certificate
    options.set_transport(Transport::tls_with_default_config());
    let (client, mut connection) = Client::new(options, 10);

    // Subscribe to the temperature topic
    client.subscribe(topic, QoS::AtLeastOnce).unwrap();
    // Publish a JSON reading
    client.publish(topic, QoS::AtLeastOnce, false, r#"{"temperature":21.5}"#).unwrap();

    // Keep the client running
    for event in connection.iter() {
        if let Ok(Event::Incoming(Packet::Publish(p))) = event {
            println!("{}: {}", p.topic, String::from_utf8_lossy(&p.payload));
        }
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
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=rust-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=rust-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=rust-footer">Pricing</a> ·
  <a href="https://connectmq.com/code-samples/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=rust-footer">All code samples</a>
</p>
