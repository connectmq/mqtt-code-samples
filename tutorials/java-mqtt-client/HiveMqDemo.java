import java.nio.charset.StandardCharsets;
import java.time.Instant;

import com.hivemq.client.mqtt.MqttClient;
import com.hivemq.client.mqtt.datatypes.MqttQos;
import com.hivemq.client.mqtt.mqtt5.Mqtt5AsyncClient;

public class HiveMqDemo {

    static String env(String key, String def) {
        String v = System.getenv(key);
        return (v == null || v.isEmpty()) ? def : v;
    }

    public static void main(String[] args) throws Exception {
        String host = env("MQTT_HOST", "broker.connectmq.com");
        String clientId = env("MQTT_CLIENT_ID", "hivemq-j6t1ve");
        String prefix = env("MQTT_PREFIX", "connectmq/demo/j6t1ve");
        String user = System.getenv("MQTT_USERNAME");

        Mqtt5AsyncClient client = MqttClient.builder()
                .useMqttVersion5()
                .identifier(clientId)
                .serverHost(host)
                .serverPort(8883)
                .sslWithDefaultConfig()
                .automaticReconnectWithDefaultConfig()
                .addConnectedListener(ctx -> System.out.println("connected"))
                .addDisconnectedListener(ctx ->
                        System.out.println("disconnected: " + ctx.getCause().getMessage()))
                .buildAsync();

        var connect = client.connectWith()
                .cleanStart(false)
                .sessionExpiryInterval(600)
                .keepAlive(30)
                .willPublish()
                    .topic(prefix + "/status")
                    .payload("offline".getBytes(StandardCharsets.UTF_8))
                    .qos(MqttQos.AT_LEAST_ONCE)
                    .retain(true)
                    .applyWillPublish();
        if (user != null) {
            connect = connect.simpleAuth()
                    .username(user)
                    .password(env("MQTT_PASSWORD", "").getBytes(StandardCharsets.UTF_8))
                    .applySimpleAuth();
        }
        connect.send().join();

        client.subscribeWith()
                .topicFilter(prefix + "/cmd/#")
                .qos(MqttQos.AT_LEAST_ONCE)
                .callback(publish -> System.out.println("command on " + publish.getTopic() + ": "
                        + new String(publish.getPayloadAsBytes(), StandardCharsets.UTF_8)))
                .send()
                .join();

        client.publishWith()
                .topic(prefix + "/status")
                .payload("online".getBytes(StandardCharsets.UTF_8))
                .qos(MqttQos.AT_LEAST_ONCE)
                .retain(true)
                .send();

        while (true) {
            String json = String.format("{\"device\":\"%s\",\"temperature\":%.2f,\"ts\":\"%s\"}",
                    clientId, 20 + Math.random() * 5, Instant.now());
            client.publishWith()
                    .topic(prefix + "/telemetry")
                    .payload(json.getBytes(StandardCharsets.UTF_8))
                    .qos(MqttQos.AT_LEAST_ONCE)
                    .contentType("application/json")
                    .messageExpiryInterval(60)
                    .send()
                    .whenComplete((result, error) -> {
                        if (error != null) System.err.println("publish failed: " + error.getMessage());
                    });
            Thread.sleep(5000);
        }
    }
}
