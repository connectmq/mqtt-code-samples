using MQTTnet;
using MQTTnet.Formatter;

var topic = "connectmq/demo/k3x8p1/libs/csharp";
var factory = new MqttClientFactory();
using var client = factory.CreateMqttClient();

client.ApplicationMessageReceivedAsync += e =>
{
    Console.WriteLine($"{e.ApplicationMessage.Topic} {e.ApplicationMessage.ConvertPayloadToString()}");
    return Task.CompletedTask;
};

var options = new MqttClientOptionsBuilder()
    .WithTcpServer("broker.connectmq.com", 8883)
    .WithClientId($"libs-cs-{Guid.NewGuid():N}"[..16])
    .WithProtocolVersion(MqttProtocolVersion.V500)
    .WithTlsOptions(o => o.UseTls())
    .Build();

await client.ConnectAsync(options);
await client.SubscribeAsync(factory.CreateSubscribeOptionsBuilder()
    .WithTopicFilter(topic).Build());

await client.PublishAsync(new MqttApplicationMessageBuilder()
    .WithTopic(topic).WithPayload("hello from MQTTnet").Build());

await Task.Delay(2000);
await client.DisconnectAsync();
