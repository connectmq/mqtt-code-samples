<?php

require __DIR__ . '/../mqtt.php';

use PhpMqtt\Client\Exceptions\MqttClientException;
use PhpMqtt\Client\MqttClient;

$device = preg_replace('/[^a-z0-9_-]/i', '', $_POST['device'] ?? '');
$action = in_array($_POST['action'] ?? '', ['on', 'off'], true) ? $_POST['action'] : null;

if ($device === '' || $action === null) {
    http_response_code(400);
    exit('Invalid device or action');
}

$topic = mqtt_topic_prefix() . "/devices/{$device}/set";
$payload = json_encode(['action' => $action, 'ts' => time()]);

try {
    $mqtt = mqtt_client('web');
    $mqtt->connect(mqtt_settings(), true);
    $mqtt->publish($topic, $payload, MqttClient::QOS_AT_LEAST_ONCE);
    $mqtt->loop(true, true);   // wait until the PUBACK has been received
    $mqtt->disconnect();
    echo "Sent {$action} to {$device}";
} catch (MqttClientException $e) {
    error_log('MQTT publish failed: ' . $e->getMessage());
    http_response_code(502);
    echo 'Device gateway unavailable';
}
