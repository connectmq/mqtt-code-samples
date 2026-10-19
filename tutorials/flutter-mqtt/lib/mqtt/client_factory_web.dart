import 'package:mqtt_client/mqtt_client.dart';
import 'package:mqtt_client/mqtt_browser_client.dart';

MqttClient createClient(String host, String clientId) {
  final client = MqttBrowserClient.withPort('wss://$host/mqtt', clientId, 8084);
  client.websocketProtocols = MqttClientConstants.protocolsSingleDefault;
  return client;
}
