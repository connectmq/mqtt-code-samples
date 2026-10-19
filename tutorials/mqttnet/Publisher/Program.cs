using System.Text.Json;
using MQTTnet;
using MQTTnet.Formatter;
using MQTTnet.Protocol;

const string Prefix = "connectmq/demo/k7f3q9";

var factory = new MqttClientFactory();
using var client = factory.CreateMqttClient();

var options = new MqttClientOptionsBuilder()
    .WithTcpServer("broker.connectmq.com", 8883)
    .WithClientId($"pub-{Guid.NewGuid():N}")
    .WithProtocolVersion(MqttProtocolVersion.V500)
    .WithTlsOptions(o => o.UseTls())
    .WithWillTopic($"{Prefix}/sensor-1/status")
    .WithWillPayload("offline")
    .WithWillRetain(true)
    .WithWillQualityOfServiceLevel(MqttQualityOfServiceLevel.AtLeastOnce)
    .Build();

await client.ConnectAsync(options, CancellationToken.None);

// Retained "online" status: new subscribers see it immediately.
await client.PublishAsync(new MqttApplicationMessageBuilder()
    .WithTopic($"{Prefix}/sensor-1/status")
    .WithPayload("online")
    .WithRetainFlag(true)
    .WithQualityOfServiceLevel(MqttQualityOfServiceLevel.AtLeastOnce)
    .Build());

var rnd = new Random();
using var cts = new CancellationTokenSource();
Console.CancelKeyPress += (_, e) => { e.Cancel = true; cts.Cancel(); };

while (!cts.IsCancellationRequested)
{
    var reading = new
    {
        deviceId = "sensor-1",
        temperature = Math.Round(20 + rnd.NextDouble() * 5, 2),
        ts = DateTimeOffset.UtcNow.ToUnixTimeMilliseconds()
    };

    var message = new MqttApplicationMessageBuilder()
        .WithTopic($"{Prefix}/sensor-1/telemetry")
        .WithPayload(JsonSerializer.Serialize(reading))
        .WithContentType("application/json")
        .WithUserProperty("firmware", "1.4.2")
        .WithMessageExpiryInterval(60)
        .WithQualityOfServiceLevel(MqttQualityOfServiceLevel.AtLeastOnce)
        .Build();

    var pub = await client.PublishAsync(message, cts.Token);
    Console.WriteLine($"Published {reading.temperature} -> {pub.ReasonCode}");

    try { await Task.Delay(2000, cts.Token); } catch (TaskCanceledException) { }
}

await client.DisconnectAsync();
