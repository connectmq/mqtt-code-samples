import com.hivemq.client.mqtt.MqttGlobalPublishFilter
import com.hivemq.client.mqtt.datatypes.MqttQos
import com.hivemq.client.mqtt.mqtt5.Mqtt5Client
import java.util.UUID

fun main() {
    val topic = "your-project/sensors/temperature" // Use a unique topic prefix: everyone can read the public broker

    // Connect to the free public broker (no account needed) (Every client needs a unique client ID)
    val client = Mqtt5Client.builder()
        .identifier("android-" + UUID.randomUUID())
        .serverHost("broker.connectmq.com")
        .serverPort(1883)
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
