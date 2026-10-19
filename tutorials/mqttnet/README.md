# MQTTnet C# Tutorial: Build MQTT 5 Clients in .NET with TLS

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqttnet-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqttnet-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Build a .NET console publisher and subscriber with MQTTnet, MQTT 5 properties and TLS on port 8883, then add reconnect logic and move the same code to a private ConnectMQ broker.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqttnet-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqttnet-intro)

📖 **Full step-by-step tutorial:** [MQTTnet C# Tutorial: Build MQTT 5 Clients in .NET with TLS](https://connectmq.com/blog/mqttnet/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqttnet-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqttnet-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`Subscriber/Program.cs`](Subscriber/Program.cs) | MQTT 5 subscriber over TLS (8883) that subscribes to `connectmq/demo/k7f3q9/#` with QoS 1 and prints payloads, content type and user properties |
| [`Publisher/Program.cs`](Publisher/Program.cs) | MQTT 5 publisher with a retained Last Will, a retained `online` status and JSON telemetry every 2 s with content type, user property and message expiry |

## Requirements

- .NET 8 SDK or newer (`dotnet --version` to check)
- [MQTTnet](https://github.com/dotnet/MQTTnet) 5.x (the code uses the v5 API: `MqttClientFactory`, `WithTlsOptions`)
- Any editor: Visual Studio, Rider or VS Code with the C# extension
- Outbound access to port 8883 (TLS) or 1883 (plain TCP)

## Run it on the free public broker

1. Create the two console projects and add MQTTnet:

   ```bash
   mkdir MqttNetDemo && cd MqttNetDemo
   dotnet new console -n Publisher
   dotnet new console -n Subscriber
   dotnet add Publisher package MQTTnet
   dotnet add Subscriber package MQTTnet
   ```

2. Replace each generated `Program.cs` with the file from this folder, and change the `Prefix` constant `connectmq/demo/k7f3q9` to your own unique prefix in both.

3. Start the subscriber, then the publisher in another terminal:

   ```bash
   dotnet run --project Subscriber
   dotnet run --project Publisher
   ```

   The subscriber prints the JSON, the `application/json` content type and the `firmware` user property. Stop the publisher with Ctrl+C and the retained status stays `online`; kill the process instead and the broker publishes the Last Will (`offline`).

4. Optional: MQTTnet 5 has no managed client, so add the post's reconnect loop to keep a client connected with exponential backoff and jitter:

   ```csharp
   async Task KeepConnectedAsync(IMqttClient client, MqttClientOptions options,
       Func<Task> onConnected, CancellationToken ct)
   {
       var delay = TimeSpan.FromSeconds(1);
       while (!ct.IsCancellationRequested)
       {
           try
           {
               if (!await client.TryPingAsync(ct))
               {
                   await client.ConnectAsync(options, ct);
                   await onConnected();          // resubscribe here
                   Console.WriteLine("Reconnected");
                   delay = TimeSpan.FromSeconds(1);
               }
           }
           catch (Exception ex)
           {
               Console.WriteLine($"Connect failed: {ex.Message}");
               delay = TimeSpan.FromSeconds(Math.Min(delay.TotalSeconds * 2, 60));
           }
           await Task.Delay(delay + TimeSpan.FromMilliseconds(Random.Shared.Next(0, 500)), ct);
       }
   }
   ```

If the connection times out, test the port with `Test-NetConnection broker.connectmq.com -Port 8883`. Public broker limits: 64 KB per message, 10 messages per second per client, 10 subscriptions per client and up to 8 topic levels.

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqttnet-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqttnet-private) — the **Serverless (Free)** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. In `Subscriber/Program.cs` and `Publisher/Program.cs`, change the options builder to use your broker host, the generated client ID and credentials (keep the Will and keep-alive settings you need):

   ```csharp
   var options = new MqttClientOptionsBuilder()
       .WithTcpServer("YOUR_BROKER_HOST", 8883)
       .WithClientId("YOUR_CLIENT_ID")
       .WithCredentials("YOUR_USERNAME", "YOUR_PASSWORD")
       .WithProtocolVersion(MqttProtocolVersion.V500)
       .WithTlsOptions(o => o.UseTls())
       .Build();
   ```

   Keep credentials out of source code: use environment variables or `dotnet user-secrets`. Client IDs on ConnectMQ are bound to the issued credentials, so each app needs its own.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [MQTTnet C# Tutorial: Build MQTT 5 Clients in .NET with TLS](https://connectmq.com/blog/mqttnet/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqttnet-related) — the full tutorial with explanations
- 🧩 [C# basic example](../../csharp/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqttnet-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqttnet-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqttnet-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqttnet-footer">Blog</a>
</p>
