import json
import math
import random
import time
import uuid

import paho.mqtt.client as mqtt

BROKER = "broker.connectmq.com"
PREFIX = "connectmq/demo/k7f3q2"
SENSORS = ["line1", "line2", "line3"]

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=f"sim-{uuid.uuid4().hex[:8]}")
client.connect(BROKER, 1883, keepalive=60)
client.loop_start()

t = 0
try:
    while True:
        for sensor in SENSORS:
            reading = {
                "sensor": sensor,
                "temperature": round(22 + 3 * math.sin(t / 20) + random.uniform(-0.5, 0.5), 2),
                "humidity": round(45 + 5 * math.cos(t / 30) + random.uniform(-1, 1), 2),
                "ts": time.time(),
            }
            client.publish(f"{PREFIX}/sensors/{sensor}", json.dumps(reading), qos=0)
        t += 1
        time.sleep(1)
except KeyboardInterrupt:
    pass
finally:
    client.loop_stop()
    client.disconnect()
