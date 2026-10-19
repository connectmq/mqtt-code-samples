import org.eclipse.paho.client.mqttv3.*;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;

public class Example {
    public static void main(String[] args) throws Exception {
        String topic = "your-project/sensors/temperature";

        // Connect to your private ConnectMQ broker on port 8883 (TLS: the system CA store verifies the broker certificate)
        MqttClient client = new MqttClient("ssl://YOUR_BROKER_HOST:8883",
                MqttClient.generateClientId(), new MemoryPersistence());
        MqttConnectOptions options = new MqttConnectOptions();
        // Username and password from your ConnectMQ dashboard
        options.setUserName("YOUR_USERNAME");
        options.setPassword("YOUR_PASSWORD".toCharArray());
        // Reconnect automatically if the connection drops
        options.setAutomaticReconnect(true);
        client.connect(options);

        // Subscribe to the temperature topic
        client.subscribe(topic, 1, (t, message) ->
                System.out.println(t + ": " + new String(message.getPayload())));

        // Publish a JSON reading
        client.publish(topic, "{\"temperature\":21.5}".getBytes(), 1, false);
    }
}
