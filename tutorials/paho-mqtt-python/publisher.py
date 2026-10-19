import json
import random
import time
import uuid

import paho.mqtt.client as mqtt

BROKER = "broker.connectmq.com"
PORT = 1883
PREFIX = "connectmq/demo/k7f3q2"

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=f"pub-{uuid.uuid4().hex[:8]}")

# Last Will: published by the broker if this client disappears without disconnecting.
client.will_set(f"{PREFIX}/status/publisher", payload="offline", qos=1, retain=True)

client.connect(BROKER, PORT, keepalive=60)
client.loop_start()  # network loop in a background thread

# Retained status: new subscribers get it immediately.
client.publish(f"{PREFIX}/status/publisher", "online", qos=1, retain=True)

try:
    for i in range(10):
        payload = json.dumps({"seq": i, "temperature": round(random.uniform(20, 25), 2)})
        info = client.publish(f"{PREFIX}/sensors/room1", payload, qos=1)
        info.wait_for_publish(timeout=5)
        print(f"Sent #{i} (mid={info.mid}, published={info.is_published()})")
        time.sleep(1)
finally:
    client.publish(f"{PREFIX}/status/publisher", "offline", qos=1, retain=True).wait_for_publish(5)
    client.disconnect()
    client.loop_stop()
