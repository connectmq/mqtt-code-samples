# ASP.NET Core MQTT: A Background Service That Stores and Streams Device Data

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-asp-net-core-mqtt-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-asp-net-core-mqtt-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Host an MQTTnet subscriber as an ASP.NET Core BackgroundService, persist device telemetry with EF Core and push every reading to browsers over SignalR, using ConnectMQ as the broker.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-asp-net-core-mqtt-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-asp-net-core-mqtt-intro)

📖 **Full step-by-step tutorial:** [ASP.NET Core MQTT: A Background Service That Stores and Streams Device Data](https://connectmq.com/blog/asp-net-core-mqtt/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-asp-net-core-mqtt-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-asp-net-core-mqtt-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`appsettings.json`](appsettings.json) | MQTT connection settings (public broker, TLS 8883, topic filter) and the SQLite connection string. |
| [`Models.cs`](Models.cs) | `Reading` entity, `DeviceDb` EF Core context and the `MqttOptions` settings class. |
| [`TelemetryHub.cs`](TelemetryHub.cs) | Empty SignalR hub that browsers listen on. |
| [`MqttIngestService.cs`](MqttIngestService.cs) | MQTTnet `BackgroundService`: connects with backoff, subscribes, parses messages into a bounded channel, batches EF Core writes and pushes readings over SignalR. |
| [`Program.cs`](Program.cs) | Wires options, EF Core, SignalR, the hosted service, static files and the `/api/readings/{deviceId}` endpoint. |

## Requirements

- .NET SDK with `dotnet new web` (ASP.NET Core; SignalR is in the shared framework)
- NuGet packages `MQTTnet` and `Microsoft.EntityFrameworkCore.Sqlite`
- Optional: `mosquitto_pub` to publish test readings

## Run it on the free public broker

1. Create the project and add the packages:

   ```bash
   dotnet new web -n DeviceHub
   cd DeviceHub
   dotnet add package MQTTnet
   dotnet add package Microsoft.EntityFrameworkCore.Sqlite
   ```

2. Copy the files from this folder into `DeviceHub/` (replacing the generated `Program.cs` and `appsettings.json`). Change `ClientId` and the prefix in `TopicFilter` to your own random values.
3. Optional dashboard: create `wwwroot/index.html` with a `<ul id="log">` and the SignalR JavaScript client from a CDN. The essential script from the post:

   ```javascript
   const connection = new signalR.HubConnectionBuilder()
     .withUrl("/hubs/telemetry")
     .withAutomaticReconnect()
     .build();

   connection.on("reading", r => {
     const li = document.createElement("li");
     li.textContent = `${r.receivedAt} ${r.deviceId}: ${r.temperature} °C`;
     document.getElementById("log").prepend(li);
   });

   connection.start();
   ```

4. Run the app with `dotnet run`, open the page, then publish a fake reading:

   ```bash
   mosquitto_pub -h broker.connectmq.com -p 1883 -i devicehub-test-1 \
     -t connectmq/demo/8d21c4/boiler-1/telemetry -q 1 \
     -m '{"temperature": 71.4}'
   ```

   The reading appears in the browser and is returned by `/api/readings/boiler-1`.

To send commands back to devices, the post suggests a small singleton wrapper around the connected client (do not open a connection per HTTP request):

```csharp
public class MqttCommandPublisher(IMqttClient client)
{
    public Task<MqttClientPublishResult> SendAsync(string deviceId, object command,
        CancellationToken ct) =>
        client.PublishAsync(new MqttApplicationMessageBuilder()
            .WithTopic($"connectmq/demo/8d21c4/{deviceId}/cmd")
            .WithPayload(JsonSerializer.Serialize(command))
            .WithContentType("application/json")
            .WithMessageExpiryInterval(30)
            .WithQualityOfServiceLevel(MqttQualityOfServiceLevel.AtLeastOnce)
            .Build(), ct);
}
```

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-asp-net-core-mqtt-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-asp-net-core-mqtt-private) — the **Free** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. No code changes: `appsettings.json` already uses TLS on port 8883. Override the `Mqtt` section with user secrets (use the client ID generated in the portal, and keep credentials out of `appsettings.json`):

   ```bash
   dotnet user-secrets set "Mqtt:Host" "YOUR_BROKER_HOST"
   dotnet user-secrets set "Mqtt:ClientId" "YOUR_CLIENT_ID"
   dotnet user-secrets set "Mqtt:Username" "YOUR_USERNAME"
   dotnet user-secrets set "Mqtt:Password" "YOUR_PASSWORD"
   ```

   Also set `Mqtt:TopicFilter` to the topics your devices publish on.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [ASP.NET Core MQTT: A Background Service That Stores and Streams Device Data](https://connectmq.com/blog/asp-net-core-mqtt/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-asp-net-core-mqtt-related) — the full tutorial with explanations
- 🧩 [C# basic example](../../csharp/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-asp-net-core-mqtt-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-asp-net-core-mqtt-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-asp-net-core-mqtt-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-asp-net-core-mqtt-footer">Blog</a>
</p>
