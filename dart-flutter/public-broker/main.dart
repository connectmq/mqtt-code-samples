import 'dart:convert';
import 'package:mqtt_client/mqtt_client.dart';
import 'package:mqtt_client/mqtt_server_client.dart';

Future<void> main() async {
  const topic = 'your-project/sensors/temperature'; // Use a unique topic prefix: everyone can read the public broker

  // Connect to the free public broker (no account needed) (Every client needs a unique client ID)
  final client = MqttServerClient.withPort('broker.connectmq.com', 'flutter-example', 1883);
  client.keepAlivePeriod = 30;
  await client.connect();

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
