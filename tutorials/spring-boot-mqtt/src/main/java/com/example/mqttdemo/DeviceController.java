package com.example.mqttdemo;

import java.util.Collection;
import java.util.regex.Pattern;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/devices")
public class DeviceController {

    private static final Pattern SAFE_ID = Pattern.compile("[A-Za-z0-9_-]{1,64}");

    private final ReadingStore store;
    private final MqttGateway gateway;
    private final String prefix;

    public DeviceController(ReadingStore store, MqttGateway gateway,
                            @Value("${mqtt.prefix}") String prefix) {
        this.store = store;
        this.gateway = gateway;
        this.prefix = prefix;
    }

    @GetMapping
    public Collection<ReadingStore.DeviceReading> all() {
        return store.all();
    }

    @GetMapping("/{id}")
    public ResponseEntity<ReadingStore.DeviceReading> one(@PathVariable String id) {
        return ResponseEntity.of(store.get(id));
    }

    @PostMapping("/{id}/commands")
    public ResponseEntity<Void> command(@PathVariable String id, @RequestBody String body) {
        if (!SAFE_ID.matcher(id).matches()) {
            return ResponseEntity.badRequest().build();
        }
        gateway.publish(prefix + "/devices/" + id + "/cmd", body);
        return ResponseEntity.accepted().build();
    }
}
