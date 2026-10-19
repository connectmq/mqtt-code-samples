import 'dart:convert';
import 'package:mqtt_client/mqtt_client.dart';
import 'package:mqtt_client/mqtt_server_client.dart';

Future<void> main() async {
  const topic = 'your-project/sensors/temperature';

  // Connect to your private ConnectMQ broker on port 8883 (Every client needs a unique client ID)
  final client = MqttServerClient.withPort('YOUR_BROKER_HOST', 'flutter-example', 8883);
  client.keepAlivePeriod = 30;
  // TLS: the system CA store verifies the broker certificate
  client.secure = true;
  // Username and password from your ConnectMQ dashboard
  await client.connect('YOUR_USERNAME', 'YOUR_PASSWORD');

  // Subscribe to the temperature topic
  client.subscribe(topic, MqttQos.atLeastOnce);
  // Runs for every message on a subscribed topic
  client.updates!.listen((messages) {
    final message = messages.first.payload as MqttPublishMessage;
    final text = MqttPublishPayload.bytesToStringAsString(message.payload.message);
    print('${messages.first.topic}: $text');
  });

  // Publish a JSON reading
  final builder = MqttClientPayloadBuilder()..addString(jsonEncode({'temperature': 21.5}));
  client.publishMessage(topic, MqttQos.atLeastOnce, builder.payload!);
}
