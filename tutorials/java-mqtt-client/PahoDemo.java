import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

import org.eclipse.paho.mqttv5.client.IMqttToken;
import org.eclipse.paho.mqttv5.client.MqttCallback;
import org.eclipse.paho.mqttv5.client.MqttClient;
import org.eclipse.paho.mqttv5.client.MqttConnectionOptions;
import org.eclipse.paho.mqttv5.client.MqttDisconnectResponse;
import org.eclipse.paho.mqttv5.client.persist.MemoryPersistence;
import org.eclipse.paho.mqttv5.common.MqttException;
import org.eclipse.paho.mqttv5.common.MqttMessage;
import org.eclipse.paho.mqttv5.common.packet.MqttProperties;

public class PahoDemo {

    static String env(String key, String def) {
        String v = System.getenv(key);
        return (v == null || v.isEmpty()) ? def : v;
    }

    public static void main(String[] args) throws Exception {
        String serverUri = env("MQTT_URL", "ssl://broker.connectmq.com:8883");
        String clientId = env("MQTT_CLIENT_ID", "paho-j6t1ve");
        String prefix = env("MQTT_PREFIX", "connectmq/demo/j6t1ve");
        String user = System.getenv("MQTT_USERNAME");
        String commandFilter = prefix + "/cmd/#";
        ExecutorService worker = Executors.newSingleThreadExecutor();

        MqttClient client = new MqttClient(serverUri, clientId, new MemoryPersistence());

        MqttConnectionOptions options = new MqttConnectionOptions();
        options.setAutomaticReconnect(true);
        options.setCleanStart(false);
        options.setSessionExpiryInterval(600L);
        options.setKeepAliveInterval(30);
        if (user != null) {
            options.setUserName(user);
            options.setPassword(env("MQTT_PASSWORD", "").getBytes(StandardCharsets.UTF_8));
        }
        MqttMessage will = new MqttMessage("offline".getBytes(StandardCharsets.UTF_8));
        will.setQos(1);
        will.setRetained(true);
        options.setWill(prefix + "/status", will);

        client.setCallback(new MqttCallback() {
            @Override
            public void connectComplete(boolean reconnect, String uri) {
                System.out.println((reconnect ? "reconnected to " : "connected to ") + uri);
                if (reconnect) {
                    // Never block the callback thread; resubscribe on a worker.
                    worker.submit(() -> {
                        try {
                            client.subscribe(commandFilter, 1);
                        } catch (MqttException e) {
                            System.err.println("resubscribe failed: " + e.getMessage());
                        }
                    });
                }
            }

            @Override
            public void messageArrived(String topic, MqttMessage message) {
                System.out.println("command on " + topic + ": "
                        + new String(message.getPayload(), StandardCharsets.UTF_8));
            }

            @Override
            public void disconnected(MqttDisconnectResponse response) {
                System.out.println("disconnected: " + response.getReasonString());
            }

            @Override
            public void mqttErrorOccurred(MqttException exception) {
                System.err.println("error: " + exception.getMessage());
            }

            @Override
            public void deliveryComplete(IMqttToken token) { }

            @Override
            public void authPacketArrived(int reasonCode, MqttProperties properties) { }
        });

        client.connect(options);
        client.subscribe(commandFilter, 1);

        MqttMessage online = new MqttMessage("online".getBytes(StandardCharsets.UTF_8));
        online.setQos(1);
        online.setRetained(true);
        client.publish(prefix + "/status", online);

        while (true) {
            String json = String.format("{\"device\":\"%s\",\"temperature\":%.2f,\"ts\":\"%s\"}",
                    clientId, 20 + Math.random() * 5, Instant.now());
            MqttMessage msg = new MqttMessage(json.getBytes(StandardCharsets.UTF_8));
            msg.setQos(1);
            try {
                client.publish(prefix + "/telemetry", msg);
            } catch (MqttException e) {
                System.err.println("publish failed: " + e.getMessage());
            }
            Thread.sleep(5000);
        }
    }
}
