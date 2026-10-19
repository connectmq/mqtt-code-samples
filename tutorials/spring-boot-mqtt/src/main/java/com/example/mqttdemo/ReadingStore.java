package com.example.mqttdemo;

import java.nio.charset.StandardCharsets;
import java.time.Instant;
import java.util.Collection;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.integration.mqtt.support.MqttHeaders;
import org.springframework.messaging.Message;
import org.springframework.stereotype.Component;

@Component
public class ReadingStore {

    public record DeviceReading(String deviceId, JsonNode data, Instant receivedAt) { }

    private static final Logger log = LoggerFactory.getLogger(ReadingStore.class);
    private final Map<String, DeviceReading> latest = new ConcurrentHashMap<>();
    private final ObjectMapper mapper;

    public ReadingStore(ObjectMapper mapper) {
        this.mapper = mapper;
    }

    public void accept(Message<?> message) {
        String topic = message.getHeaders().get(MqttHeaders.RECEIVED_TOPIC, String.class);
        String[] parts = topic.split("/");
        String deviceId = parts[parts.length - 2];
        String json = new String((byte[]) message.getPayload(), StandardCharsets.UTF_8);
        try {
            latest.put(deviceId, new DeviceReading(deviceId, mapper.readTree(json), Instant.now()));
        } catch (JsonProcessingException e) {
            log.warn("Ignoring invalid JSON from {}: {}", deviceId, e.getOriginalMessage());
        }
    }

    public Collection<DeviceReading> all() {
        return latest.values();
    }

    public Optional<DeviceReading> get(String deviceId) {
        return Optional.ofNullable(latest.get(deviceId));
    }
}
