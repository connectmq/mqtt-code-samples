# Go MQTT Example

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=go-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=go-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../LICENSE)

Connect Go to an MQTT broker with the Eclipse Paho Go client. Start on the free public broker, then point the same code at a secure private broker on ConnectMQ.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=go-intro)** — the managed, serverless MQTT broker for IoT. Try this example on the free public broker in seconds, then move the very same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=go-intro)

Full walkthrough on the website: **[Go MQTT example](https://connectmq.com/code-samples/go/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=go-intro)**

## Requirements

- **Library:** [Eclipse Paho Go](https://github.com/eclipse/paho.mqtt.golang)
- **Install:**

```bash
go get github.com/eclipse/paho.mqtt.golang
```

## Files

| Folder | Broker | What it does |
| --- | --- | --- |
| [`public-broker/`](public-broker/) | Free public broker `broker.connectmq.com` | Connect without an account, subscribe and publish a JSON reading |
| [`private-broker/`](private-broker/) | Your private ConnectMQ broker | The same flow over TLS with your username and password |

## How to run

```bash
cd public-broker   # or private-broker
go mod init mqtt-example
go get github.com/eclipse/paho.mqtt.golang
go run main.go
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

**`main.go`** ([open file](public-broker/main.go))

```go
package main

import (
	"fmt"
	"time"

	mqtt "github.com/eclipse/paho.mqtt.golang"
)

func main() {
	topic := "your-project/sensors/temperature" // Use a unique topic prefix: everyone can read the public broker

	// Connect to the free public broker (no account needed)
	opts := mqtt.NewClientOptions().AddBroker("tcp://broker.connectmq.com:1883")
	// Every client needs a unique client ID
	opts.SetClientID(fmt.Sprintf("go-%d", time.Now().UnixNano()))
	// Reconnect automatically if the connection drops
	opts.SetAutoReconnect(true)
	// Runs when the connection is established
	opts.SetOnConnectHandler(func(c mqtt.Client) {
		// Subscribe to the temperature topic
		c.Subscribe(topic, 1, func(_ mqtt.Client, m mqtt.Message) {
			fmt.Printf("%s: %s\n", m.Topic(), m.Payload())
		})
	})

	client := mqtt.NewClient(opts)
	if t := client.Connect(); t.Wait() && t.Error() != nil {
		panic(t.Error())
	}
	// Publish a JSON reading
	client.Publish(topic, 1, false, `{"temperature":21.5}`).Wait()
	// Keep the client running
	select {}
}
```

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic, including yours. Never send passwords, personal data or anything confidential through it, and use a unique topic prefix (`your-project/...`) so your messages don't mix with others'. There is no guarantee of availability or message retention. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=go-public)

## 2. Go to production with a private ConnectMQ broker

For real devices, use a private serverless MQTT broker on ConnectMQ instead of the public one: TLS encryption, a username and password for every device and per-topic access control, fully managed. The Serverless (Free) plan needs no credit card.

**Get your private broker in under a minute:**

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=go-private) — no credit card.
2. Create a broker in the dashboard (the **Serverless (Free)** plan is enough to start).
3. Copy the **host**, **username** and **password** of your broker.
4. Replace `YOUR_BROKER_HOST`, `YOUR_USERNAME` and `YOUR_PASSWORD` in the files under [`private-broker/`](private-broker/) and run them.

**`main.go`** ([open file](private-broker/main.go))

```go
package main

import (
	"crypto/tls"
	"fmt"
	"time"

	mqtt "github.com/eclipse/paho.mqtt.golang"
)

func main() {
	topic := "your-project/sensors/temperature"

	// Connect to your private ConnectMQ broker on port 8883
	opts := mqtt.NewClientOptions().AddBroker("ssl://YOUR_BROKER_HOST:8883")
	// Username and password from your ConnectMQ dashboard
	opts.SetUsername("YOUR_USERNAME")
	opts.SetPassword("YOUR_PASSWORD")
	// TLS: the system CA store verifies the broker certificate
	opts.SetTLSConfig(&tls.Config{MinVersion: tls.VersionTLS12})
	// Every client needs a unique client ID
	opts.SetClientID(fmt.Sprintf("go-%d", time.Now().UnixNano()))
	// Reconnect automatically if the connection drops
	opts.SetAutoReconnect(true)
	// Runs when the connection is established
	opts.SetOnConnectHandler(func(c mqtt.Client) {
		// Subscribe to the temperature topic
		c.Subscribe(topic, 1, func(_ mqtt.Client, m mqtt.Message) {
			fmt.Printf("%s: %s\n", m.Topic(), m.Payload())
		})
	})

	client := mqtt.NewClient(opts)
	if t := client.Connect(); t.Wait() && t.Error() != nil {
		panic(t.Error())
	}
	// Publish a JSON reading
	client.Publish(topic, 1, false, `{"temperature":21.5}`).Wait()
	// Keep the client running
	select {}
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
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=go-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=go-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=go-footer">Pricing</a> ·
  <a href="https://connectmq.com/code-samples/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=go-footer">All code samples</a>
</p>
