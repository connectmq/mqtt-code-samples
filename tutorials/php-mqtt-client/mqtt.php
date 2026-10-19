<?php

require __DIR__ . '/vendor/autoload.php';

use PhpMqtt\Client\ConnectionSettings;
use PhpMqtt\Client\MqttClient;

const MQTT_HOST = 'broker.connectmq.com';
const MQTT_PORT = 8883;

function mqtt_topic_prefix(): string
{
    return getenv('MQTT_TOPIC_PREFIX') ?: 'connectmq/demo/php-5e19c2';
}

function mqtt_client(string $role): MqttClient
{
    $clientId = getenv('MQTT_CLIENT_ID') ?: sprintf('php-%s-%s', $role, bin2hex(random_bytes(4)));
    return new MqttClient(MQTT_HOST, MQTT_PORT, $clientId, MqttClient::MQTT_3_1_1);
}

function mqtt_settings(bool $reconnect = false): ConnectionSettings
{
    $settings = (new ConnectionSettings())
        ->setUseTls(true)
        ->setTlsVerifyPeer(true)
        ->setTlsVerifyPeerName(true)
        ->setConnectTimeout(10)
        ->setSocketTimeout(5)
        ->setKeepAliveInterval(30);

    if ($user = getenv('MQTT_USERNAME')) {
        $settings = $settings
            ->setUsername($user)
            ->setPassword(getenv('MQTT_PASSWORD') ?: null);
    }

    if ($reconnect) {
        $settings = $settings
            ->setReconnectAutomatically(true)
            ->setMaxReconnectAttempts(10)
            ->setDelayBetweenReconnectAttempts(3000);
    }

    return $settings;
}
