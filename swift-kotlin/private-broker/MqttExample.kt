import com.hivemq.client.mqtt.MqttGlobalPublishFilter
import com.hivemq.client.mqtt.datatypes.MqttQos
import com.hivemq.client.mqtt.mqtt5.Mqtt5Client
import java.util.UUID

fun main() {
    val topic = "your-project/sensors/temperature"

    // Connect to your private ConnectMQ broker on port 8883 (Every client needs a unique client ID)
    val client = Mqtt5Client.builder()
        .identifier("android-" + UUID.randomUUID())
        .serverHost("YOUR_BROKER_HOST")
        .serverPort(8883)
        // TLS: the system CA store verifies the broker certificate
        .sslWithDefaultConfig()
        // Username and password from your ConnectMQ dashboard
        .simpleAuth().username("YOUR_USERNAME").password("YOUR_PASSWORD".toByteArray()).applySimpleAuth()
        .automaticReconnectWithDefaultConfig()
        .buildBlocking()
    client.connect()

    // Runs for every message on a subscribed topic
    client.toAsync().publishes(MqttGlobalPublishFilter.ALL) { p ->
        println("${p.topic}: ${String(p.payloadAsBytes)}")
    }
    // Subscribe to the temperature topic
    client.subscribeWith().topicFilter(topic).qos(MqttQos.AT_LEAST_ONCE).send()
    // Publish a JSON reading
    client.publishWith().topic(topic).qos(MqttQos.AT_LEAST_ONCE)
        .payload("""{"temperature":21.5}""".toByteArray()).send()
}
