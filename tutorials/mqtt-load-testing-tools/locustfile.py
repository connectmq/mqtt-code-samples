# locustfile.py  (pip install locust paho-mqtt)
import json
import os
import random
import time
import uuid

import paho.mqtt.client as mqtt
from locust import User, between, events, task

HOST = os.environ.get("MQTT_HOST", "YOUR_BROKER_HOST")
USER = os.environ.get("MQTT_USER", "YOUR_USERNAME")
PASS = os.environ.get("MQTT_PASS", "YOUR_PASSWORD")


class MqttDevice(User):
    wait_time = between(1, 2)

    def on_start(self):
        self.device_id = uuid.uuid4().hex[:8]
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2,
                                  client_id=f"lt-{self.device_id}",
                                  protocol=mqtt.MQTTv5)
        self.client.username_pw_set(USER, PASS)
        self.client.tls_set()
        start = time.perf_counter()
        try:
            self.client.connect(HOST, 8883, keepalive=30)
            self.client.loop_start()
            events.request.fire(request_type="MQTT", name="connect",
                                response_time=(time.perf_counter() - start) * 1000,
                                response_length=0, exception=None, context={})
        except Exception as exc:
            events.request.fire(request_type="MQTT", name="connect",
                                response_time=(time.perf_counter() - start) * 1000,
                                response_length=0, exception=exc, context={})
            raise

    @task
    def publish_telemetry(self):
        payload = json.dumps({"id": self.device_id,
                              "temp": round(random.uniform(18, 26), 2),
                              "ts": time.time()})
        start = time.perf_counter()
        info = self.client.publish(f"loadtest/device/{self.device_id}", payload, qos=1)
        exc = None
        try:
            info.wait_for_publish(timeout=5)  # waits for PUBACK at QoS 1
            if not info.is_published():
                exc = TimeoutError("no PUBACK within 5 s")
        except Exception as e:
            exc = e
        events.request.fire(request_type="MQTT", name="publish qos1",
                            response_time=(time.perf_counter() - start) * 1000,
                            response_length=len(payload), exception=exc, context={})

    def on_stop(self):
        self.client.loop_stop()
        self.client.disconnect()
