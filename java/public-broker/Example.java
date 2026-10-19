import org.eclipse.paho.client.mqttv3.*;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;

public class Example {
    public static void main(String[] args) throws Exception {
        String topic = "your-project/sensors/temperature"; // Use a unique topic prefix: everyone can read the public broker

        // Connect to the free public broker (no account needed)
        MqttClient client = new MqttClient("tcp://broker.connectmq.com:1883",
                MqttClient.generateClientId(), new MemoryPersistence());
        MqttConnectOptions options = new MqttConnectOptions();
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
