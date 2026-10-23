# .NET MAUI MQTT App: Monitor and Control Devices on Android, iOS and Windows

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-net-maui-mqtt-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-net-maui-mqtt-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Build one cross-platform .NET MAUI app with MQTTnet that displays live telemetry and sends commands to devices, handles app lifecycle reconnects and runs against a ConnectMQ broker.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-net-maui-mqtt-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-net-maui-mqtt-intro)

📖 **Full step-by-step tutorial:** [.NET MAUI MQTT App: Monitor and Control Devices on Android, iOS and Windows](https://connectmq.com/blog/net-maui-mqtt/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-net-maui-mqtt-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-net-maui-mqtt-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`MainViewModel.cs`](MainViewModel.cs) | View model owning one MQTTnet client: TLS on 8883, MQTT 5, subscribes to temperature/status/relay state, publishes relay commands, marshals updates to the main thread |
| [`MainPage.xaml`](MainPage.xaml) | Page with connection text, temperature, device status, relay switch and a Reconnect button |
| [`MainPage.xaml.cs`](MainPage.xaml.cs) | Code-behind that receives the view model through DI and connects in `OnAppearing` |

## Requirements

- .NET 8 or 9 SDK with the MAUI workload (`dotnet workload install maui`)
- [MQTTnet](https://github.com/dotnet/MQTTnet) 5.x
- CommunityToolkit.Mvvm (optional but used by the view model)
- Optional: `mosquitto_pub` / `mosquitto_sub` to simulate the device

## Run it on the free public broker

1. Create the project and add the packages:

   ```bash
   dotnet new maui -n DeviceControl
   cd DeviceControl
   dotnet add package MQTTnet
   dotnet add package CommunityToolkit.Mvvm
   ```

2. Copy `MainViewModel.cs`, `MainPage.xaml` and `MainPage.xaml.cs` into the project (replace the template's page). Change the prefix `connectmq/demo/m4ui7x` to your own.

3. Register both in `MauiProgram.cs`:

   ```csharp
   builder.Services.AddSingleton<MainViewModel>();
   builder.Services.AddSingleton<MainPage>();
   ```

   and make sure `AppShell` resolves the page from DI (the default template's `ShellContent` with `ContentTemplate` works once the page is registered).

4. Handle the app lifecycle in `App.xaml.cs` by overriding `CreateWindow`:

   ```csharp
   protected override Window CreateWindow(IActivationState? activationState)
   {
       var window = new Window(new AppShell());
       var vm = activationState!.Context.Services.GetRequiredService<MainViewModel>();
       window.Stopped += async (_, _) => await vm.DisconnectAsync();
       window.Resumed += async (_, _) => await vm.ConnectAsync();
       return window;
   }
   ```

5. Run the app on Android, iOS or Windows, then simulate the device from a terminal:

   ```bash
   # Retained presence and relay state
   mosquitto_pub -h broker.connectmq.com -p 1883 -i dev1-sim-a -r -t connectmq/demo/m4ui7x/device1/status -m online
   mosquitto_pub -h broker.connectmq.com -p 1883 -i dev1-sim-b -r -t connectmq/demo/m4ui7x/device1/relay/state -m off

   # Temperature reading
   mosquitto_pub -h broker.connectmq.com -p 1883 -i dev1-sim-c -t connectmq/demo/m4ui7x/device1/temperature -m '{"value": 22.4}'

   # Watch the commands the app sends
   mosquitto_sub -h broker.connectmq.com -p 1883 -i dev1-sim-d -t connectmq/demo/m4ui7x/device1/relay/set -v
   ```

   Tap the switch and the command appears in the last terminal; publish `on` to `relay/state` and the switch confirms.

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-net-maui-mqtt-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-net-maui-mqtt-private) — the **Free** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. In the `MainViewModel` constructor in `MainViewModel.cs`, point `WithTcpServer` at your broker host (keep port 8883 and `WithTlsOptions`), and add the generated credentials and client ID to the options builder:

   ```csharp
   .WithTcpServer("YOUR_BROKER_HOST", 8883)
   .WithCredentials("YOUR_USERNAME", "YOUR_PASSWORD")
   .WithClientId("YOUR_CLIENT_ID")
   ```

   A mobile binary can be decompiled: never embed a shared admin password. Issue one credential per user or installation from your backend, or route commands through your own API, and store any credential the app holds in `SecureStorage`, not `Preferences`.

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [.NET MAUI MQTT App: Monitor and Control Devices on Android, iOS and Windows](https://connectmq.com/blog/net-maui-mqtt/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-net-maui-mqtt-related) — the full tutorial with explanations
- 🧩 [C# basic example](../../csharp/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-net-maui-mqtt-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-net-maui-mqtt-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-net-maui-mqtt-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-net-maui-mqtt-footer">Blog</a>
</p>
