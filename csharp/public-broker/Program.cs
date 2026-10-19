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
