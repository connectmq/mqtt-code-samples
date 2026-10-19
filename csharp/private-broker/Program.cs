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
