using System.Text;
using MQTTnet;
using MQTTnet.Formatter;
using MQTTnet.Protocol;

const string Prefix = "connectmq/demo/k7f3q9";

var factory = new MqttClientFactory();
using var client = factory.CreateMqttClient();

var options = new MqttClientOptionsBuilder()
    .WithTcpServer("broker.connectmq.com", 8883)
    .WithClientId($"sub-{Guid.NewGuid():N}")
    .WithProtocolVersion(MqttProtocolVersion.V500)
    .WithTlsOptions(o => o.UseTls())
    .WithCleanStart(true)
    .WithKeepAlivePeriod(TimeSpan.FromSeconds(30))
    .Build();

client.ApplicationMessageReceivedAsync += e =>
{
    var msg = e.ApplicationMessage;
    var payload = msg.ConvertPayloadToString();
    Console.WriteLine($"[{DateTime.Now:HH:mm:ss}] {msg.Topic} (QoS {(int)msg.QualityOfServiceLevel}, retain={msg.Retain})");
    Console.WriteLine($"  payload: {payload}");
    if (!string.IsNullOrEmpty(msg.ContentType))
        Console.WriteLine($"  content-type: {msg.ContentType}");
    foreach (var p in msg.UserProperties ?? [])
        Console.WriteLine($"  user-property: {p.Name}={p.Value}");
    return Task.CompletedTask;
};

var result = await client.ConnectAsync(options, CancellationToken.None);
Console.WriteLine($"Connected: {result.ResultCode}");

var subscribe = new MqttClientSubscribeOptionsBuilder()
    .WithTopicFilter(f => f
        .WithTopic($"{Prefix}/#")
        .WithQualityOfServiceLevel(MqttQualityOfServiceLevel.AtLeastOnce))
    .Build();

var subResult = await client.SubscribeAsync(subscribe, CancellationToken.None);
foreach (var item in subResult.Items)
    Console.WriteLine($"Subscribed {item.TopicFilter.Topic}: {item.ResultCode}");

Console.WriteLine("Waiting for messages. Press Enter to exit.");
Console.ReadLine();

await client.DisconnectAsync(new MqttClientDisconnectOptionsBuilder()
    .WithReason(MqttClientDisconnectOptionsReason.NormalDisconnection)
    .Build());
