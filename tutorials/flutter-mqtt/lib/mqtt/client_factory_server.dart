import 'package:mqtt_client/mqtt_client.dart';
import 'package:mqtt_client/mqtt_server_client.dart';

MqttClient createClient(String host, String clientId) {
  final client = MqttServerClient.withPort(host, clientId, 8883);
  client.secure = true; // TLS, validated against the system trust store
  return client;
}
