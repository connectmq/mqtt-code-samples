package com.example.mqttdemo;

import java.nio.charset.StandardCharsets;

import org.eclipse.paho.mqttv5.client.MqttConnectionOptions;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.integration.annotation.IntegrationComponentScan;
import org.springframework.integration.annotation.ServiceActivator;
import org.springframework.integration.dsl.IntegrationFlow;
import org.springframework.integration.mqtt.core.Mqttv5ClientManager;
import org.springframework.integration.mqtt.inbound.Mqttv5PahoMessageDrivenChannelAdapter;
import org.springframework.integration.mqtt.outbound.Mqttv5PahoMessageHandler;
import org.springframework.messaging.MessageHandler;

@Configuration
@IntegrationComponentScan
public class MqttConfig {

    @Bean
    public Mqttv5ClientManager mqttClientManager(
            @Value("${mqtt.url}") String url,
            @Value("${mqtt.client-id}") String clientId,
            @Value("${mqtt.username}") String username,
            @Value("${mqtt.password}") String password) {
        MqttConnectionOptions options = new MqttConnectionOptions();
        options.setServerURIs(new String[] { url });
        options.setAutomaticReconnect(true);
        options.setCleanStart(false);
        options.setSessionExpiryInterval(600L);
        options.setKeepAliveInterval(30);
        if (!username.isBlank()) {
            options.setUserName(username);
            options.setPassword(password.getBytes(StandardCharsets.UTF_8));
        }
        return new Mqttv5ClientManager(options, clientId);
    }

    @Bean
    public Mqttv5PahoMessageDrivenChannelAdapter mqttInbound(
            Mqttv5ClientManager clientManager,
            @Value("${mqtt.prefix}") String prefix) {
        Mqttv5PahoMessageDrivenChannelAdapter adapter =
                new Mqttv5PahoMessageDrivenChannelAdapter(clientManager, prefix + "/devices/+/telemetry");
        adapter.setQos(1);
        return adapter;
    }

    @Bean
    public IntegrationFlow telemetryFlow(Mqttv5PahoMessageDrivenChannelAdapter mqttInbound,
                                         ReadingStore store) {
        return IntegrationFlow.from(mqttInbound)
                .handle(message -> store.accept(message))
                .get();
    }

    @Bean
    @ServiceActivator(inputChannel = "mqttOutbound")
    public MessageHandler mqttOutboundHandler(Mqttv5ClientManager clientManager) {
        Mqttv5PahoMessageHandler handler = new Mqttv5PahoMessageHandler(clientManager);
        handler.setAsync(true);
        handler.setDefaultQos(1);
        return handler;
    }
}
