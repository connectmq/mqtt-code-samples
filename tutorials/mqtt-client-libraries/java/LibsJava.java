import org.eclipse.paho.client.mqttv3.*;
import org.eclipse.paho.client.mqttv3.persist.MemoryPersistence;
import java.util.UUID;

public class LibsJava {
    public static void main(String[] args) throws Exception {
        String topic = "connectmq/demo/k3x8p1/libs/java";
        String clientId = "libs-java-" + UUID.randomUUID().toString().substring(0, 8);

        MqttClient client = new MqttClient("ssl://broker.connectmq.com:8883",
                clientId, new MemoryPersistence());
        MqttConnectOptions options = new MqttConnectOptions();
        options.setAutomaticReconnect(true);
        options.setCleanSession(true);
        client.connect(options);

        client.subscribe(topic, 1, (t, msg) ->
                System.out.println(t + " " + new String(msg.getPayload())));
        client.publish(topic, "hello from Paho Java".getBytes(), 1, false);

        Thread.sleep(2000);
        client.disconnect();
        client.close();
    }
}
