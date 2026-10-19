package com.example.mqttdemo;

import org.springframework.integration.annotation.MessagingGateway;
import org.springframework.integration.mqtt.support.MqttHeaders;
import org.springframework.messaging.handler.annotation.Header;

@MessagingGateway(defaultRequestChannel = "mqttOutbound")
public interface MqttGateway {
    void publish(@Header(MqttHeaders.TOPIC) String topic, String payload);
}
