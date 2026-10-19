<?php

require __DIR__ . '/../mqtt.php';

use PhpMqtt\Client\Exceptions\MqttClientException;
use PhpMqtt\Client\MqttClient;

pcntl_async_signals(true);

$mqtt = mqtt_client('worker');

$stop = function () use ($mqtt) {
    fwrite(STDOUT, "Shutting down...\n");
    $mqtt->interrupt();
};
pcntl_signal(SIGINT, $stop);
pcntl_signal(SIGTERM, $stop);

$filter = mqtt_topic_prefix() . '/devices/+/telemetry';

try {
    $mqtt->connect(mqtt_settings(reconnect: true), true);

    $mqtt->subscribe($filter, function (string $topic, string $message, bool $retained) {
        $parts = explode('/', $topic);
        $device = $parts[count($parts) - 2] ?? 'unknown';
        $data = json_decode($message, true);

        if (!is_array($data)) {
            fwrite(STDERR, "Ignoring non-JSON payload on {$topic}\n");
            return;
        }

        // Replace with your own persistence, e.g. PDO insert or a framework model
        printf("[%s] %s%s %s\n", date('c'), $device, $retained ? ' (retained)' : '', json_encode($data));
    }, MqttClient::QOS_AT_LEAST_ONCE);

    fwrite(STDOUT, "Subscribed to {$filter}\n");
    $mqtt->loop(true);
    $mqtt->disconnect();
} catch (MqttClientException $e) {
    fwrite(STDERR, 'MQTT error: ' . $e->getMessage() . "\n");
    exit(1);
}
