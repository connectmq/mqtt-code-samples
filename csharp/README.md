# C# (.NET) MQTT Example

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=csharp-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=csharp-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../LICENSE)

Connect C# and .NET to an MQTT broker with MQTTnet. Start on the free public broker, then point the same code at a secure private broker on ConnectMQ.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=csharp-intro)** — the managed, serverless MQTT broker for IoT. Try this example on the free public broker in seconds, then move the very same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=csharp-intro)

Full walkthrough on the website: **[C# (.NET) MQTT example](https://connectmq.com/code-samples/csharp/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=csharp-intro)**

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=csharp-hero"><img src="../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## Requirements

- **Library:** [MQTTnet 4](https://github.com/dotnet/MQTTnet)
- **Install:**

```bash
dotnet add package MQTTnet --version 4.3.7.1207
```

## Files

| Folder | Broker | What it does |
| --- | --- | --- |
| [`public-broker/`](public-broker/) | Free public broker `broker.connectmq.com` | Connect without an account, subscribe and publish a JSON reading |
| [`private-broker/`](private-broker/) | Your private ConnectMQ broker | The same flow over TLS with your username and password |

## How to run

```bash
cd public-broker   # or private-broker
dotnet new console -n MqttExample && cd MqttExample
dotnet add package MQTTnet --version 4.3.7.1207
# replace Program.cs with this folder's Program.cs
dotnet run
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

**`Program.cs`** ([open file](public-broker/Program.cs))

```csharp
using MQTTnet;
using MQTTnet.Client;

var topic = "your-project/sensors/temperature"; // Use a unique topic prefix: everyone can read the public broker
var client = new MqttFactory().CreateMqttClient();

// Runs for every message on a subscribed topic
client.ApplicationMessageReceivedAsync += e =>
{
    Console.WriteLine($"{e.ApplicationMessage.Topic}: {e.ApplicationMessage.ConvertPayloadToString()}");
    return Task.CompletedTask;
};

// Connect to the free public broker (no account needed)
var options = new MqttClientOptionsBuilder()
    .WithTcpServer("broker.connectmq.com", 1883)
    .Build();
await client.ConnectAsync(options);

// Subscribe to the temperature topic
await client.SubscribeAsync(topic);
// Publish a JSON reading
await client.PublishStringAsync(topic, "{\"temperature\":21.5}");

// Keep the client running
Console.ReadLine();
```

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic, including yours. Never send passwords, personal data or anything confidential through it, and use a unique topic prefix (`your-project/...`) so your messages don't mix with others'. There is no guarantee of availability or message retention. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=csharp-public)

## 2. Go to production with a private ConnectMQ broker

For real devices, use a private serverless MQTT broker on ConnectMQ instead of the public one: TLS encryption, a username and password for every device and per-topic access control, fully managed. The Serverless (Free) plan needs no credit card.

**Get your private broker in under a minute:**

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=csharp-private) — no credit card.
2. Create a broker in the dashboard (the **Serverless (Free)** plan is enough to start).
3. Copy the **host**, **username** and **password** of your broker.
4. Replace `YOUR_BROKER_HOST`, `YOUR_USERNAME` and `YOUR_PASSWORD` in the files under [`private-broker/`](private-broker/) and run them.

**`Program.cs`** ([open file](private-broker/Program.cs))

```csharp
using MQTTnet;
using MQTTnet.Client;

var topic = "your-project/sensors/temperature";
var client = new MqttFactory().CreateMqttClient();

// Runs for every message on a subscribed topic
client.ApplicationMessageReceivedAsync += e =>
{
    Console.WriteLine($"{e.ApplicationMessage.Topic}: {e.ApplicationMessage.ConvertPayloadToString()}");
    return Task.CompletedTask;
};

// Connect to your private ConnectMQ broker on port 8883
var options = new MqttClientOptionsBuilder()
    .WithTcpServer("YOUR_BROKER_HOST", 8883)
    // Username and password from your ConnectMQ dashboard
    .WithCredentials("YOUR_USERNAME", "YOUR_PASSWORD")
    // TLS: the system CA store verifies the broker certificate
    .WithTlsOptions(o => o.UseTls())
    .Build();
await client.ConnectAsync(options);

// Subscribe to the temperature topic
await client.SubscribeAsync(topic);
// Publish a JSON reading
await client.PublishStringAsync(topic, "{\"temperature\":21.5}");

// Keep the client running
Console.ReadLine();
```

### What you get with a private broker

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Devices & connections dashboard** — live device status, last values, connection history
- ⚡ **Fully managed and serverless** — no servers to patch or scale

<table>
  <tr>
    <td width="50%" valign="top"><a href="https://connectmq.com/monitoring/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=csharp-gallery"><img src="../assets/dashboard.png" alt="ConnectMQ dashboard: broker status, ISA-95 topic tree and live value cards with sparklines for every topic" width="100%"></a><br><b>Live dashboard</b> — broker status, ISA-95 topic tree and a live card for every topic</td>
    <td width="50%" valign="top"><a href="https://connectmq.com/digital-twin/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=csharp-gallery"><img src="../assets/digital-twin.png" alt="ConnectMQ 3D Digital Twin: machines bound to their MQTT topics with live telemetry" width="100%"></a><br><b>3D Digital Twin</b> — machines bound to their MQTT topics, telemetry on the equipment</td>
  </tr>
  <tr>
    <td width="50%" valign="top"><a href="https://connectmq.com/rules-alerts/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=csharp-gallery"><img src="../assets/rules.png" alt="ConnectMQ alert rules: conditions on JSON payload fields with message templates" width="100%"></a><br><b>Rules</b> — thresholds on JSON payload fields, such as <code>{temp} &gt; 70</code></td>
    <td width="50%" valign="top"><a href="https://connectmq.com/rules-alerts/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=csharp-gallery"><img src="../assets/alerts.png" alt="ConnectMQ triggered alerts: audit log with the exact payload that caused each alert" width="100%"></a><br><b>Alerts</b> — audit log with the exact payload, plus browser notifications</td>
  </tr>
</table>

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
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=csharp-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=csharp-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=csharp-footer">Pricing</a> ·
  <a href="https://connectmq.com/code-samples/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=csharp-footer">All code samples</a>
</p>
