import 'dart:async';
import 'dart:convert';
import 'dart:math';

import 'package:mqtt_client/mqtt_client.dart';
import 'client_factory.dart';

class MqttService {
  MqttService({
    this.host = 'broker.connectmq.com',
    this.username,
    this.password,
    String? clientId,
    String? topicPrefix,
  })  : clientId = clientId ?? 'flutter-${Random().nextInt(1000000000)}',
        topicPrefix = topicPrefix ?? 'connectmq/demo/${Random().nextInt(1000000000)}';

  final String host;
  final String? username;
  final String? password;
  final String clientId;
  final String topicPrefix;

  late final MqttClient _client;
  final _temperature = StreamController<double>.broadcast();
  final _connected = StreamController<bool>.broadcast();

  Stream<double> get temperature => _temperature.stream;
  Stream<bool> get connected => _connected.stream;

  String get sensorTopic => '$topicPrefix/sensor/temperature';
  String get relayTopic => '$topicPrefix/relay/set';

  Future<void> connect() async {
    _client = createClient(host, clientId);
    _client.keepAlivePeriod = 30;
    _client.autoReconnect = true;
    _client.resubscribeOnAutoReconnect = true;
    _client.logging(on: false);

    _client.onConnected = () => _connected.add(true);
    _client.onDisconnected = () => _connected.add(false);
    _client.onAutoReconnected = () => _connected.add(true);

    final connMessage = MqttConnectMessage()
        .withClientIdentifier(clientId)
        .startClean();
    if (username != null && password != null) {
      connMessage.authenticateAs(username!, password!);
    }
    _client.connectionMessage = connMessage;

    try {
      await _client.connect();
    } on Exception {
      _client.disconnect();
      rethrow;
    }

    if (_client.connectionStatus?.state != MqttConnectionState.connected) {
      throw StateError('MQTT connect failed: ${_client.connectionStatus}');
    }

    _client.subscribe(sensorTopic, MqttQos.atLeastOnce);
    _client.updates!.listen(_onMessages);
  }

  void _onMessages(List<MqttReceivedMessage<MqttMessage?>> messages) {
    for (final m in messages) {
      final publish = m.payload as MqttPublishMessage;
      final text = MqttPublishPayload.bytesToStringAsString(publish.payload.message);
      try {
        final value = (jsonDecode(text)['value'] as num).toDouble();
        _temperature.add(value);
      } catch (_) {
        // Ignore malformed payloads instead of crashing the stream.
      }
    }
  }

  void setRelay(bool on) {
    final builder = MqttClientPayloadBuilder()..addString(on ? 'ON' : 'OFF');
    _client.publishMessage(relayTopic, MqttQos.atLeastOnce, builder.payload!);
  }

  void dispose() {
    _client.disconnect();
    _temperature.close();
    _connected.close();
  }
}
