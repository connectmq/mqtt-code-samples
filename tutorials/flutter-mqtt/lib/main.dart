import 'package:flutter/material.dart';
import 'mqtt/mqtt_service.dart';

void main() => runApp(const MaterialApp(home: DeviceScreen()));

class DeviceScreen extends StatefulWidget {
  const DeviceScreen({super.key});
  @override
  State<DeviceScreen> createState() => _DeviceScreenState();
}

class _DeviceScreenState extends State<DeviceScreen> {
  final mqtt = MqttService();
  bool relayOn = false;
  String? error;

  @override
  void initState() {
    super.initState();
    mqtt.connect().catchError((e) => setState(() => error = '$e'));
  }

  @override
  void dispose() {
    mqtt.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Flutter MQTT Demo')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            StreamBuilder<bool>(
              stream: mqtt.connected,
              initialData: false,
              builder: (_, s) => Chip(
                label: Text(s.data! ? 'Connected' : 'Disconnected'),
              ),
            ),
            if (error != null) Text(error!, style: const TextStyle(color: Colors.red)),
            const SizedBox(height: 24),
            StreamBuilder<double>(
              stream: mqtt.temperature,
              builder: (_, s) => Text(
                s.hasData ? '${s.data!.toStringAsFixed(1)} °C' : '-- °C',
                style: Theme.of(context).textTheme.displayMedium,
              ),
            ),
            const SizedBox(height: 24),
            SwitchListTile(
              title: const Text('Relay'),
              value: relayOn,
              onChanged: (v) {
                setState(() => relayOn = v);
                mqtt.setRelay(v);
              },
            ),
            const SizedBox(height: 24),
            SelectableText('Topic prefix: ${mqtt.topicPrefix}'),
          ],
        ),
      ),
    );
  }
}
