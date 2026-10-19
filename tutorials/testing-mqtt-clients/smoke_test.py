import os
import sys
import threading
import uuid

import paho.mqtt.client as mqtt

HOST = os.getenv("MQTT_HOST", "broker.connectmq.com")
USER = os.getenv("MQTT_USERNAME")
PASSWORD = os.getenv("MQTT_PASSWORD")
CLIENT_ID = os.getenv("MQTT_CLIENT_ID") or f"smoke-{uuid.uuid4().hex[:8]}"
TOPIC = f"{os.getenv('MQTT_PREFIX', 'connectmq/demo')}/smoke-{uuid.uuid4().hex[:8]}/ping"

got = threading.Event()
nonce = uuid.uuid4().hex
errors = []


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        errors.append(f"connect failed: {reason_code}")
        got.set()  # wake the main thread; callbacks cannot exit the process
        return
    client.subscribe(TOPIC, qos=1)


def on_subscribe(client, userdata, mid, reason_codes, properties):
    client.publish(TOPIC, nonce, qos=1)


def on_message(client, userdata, msg):
    if msg.payload.decode() == nonce:
        got.set()


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=CLIENT_ID,
                     protocol=mqtt.MQTTv5)
if USER:
    client.username_pw_set(USER, PASSWORD)
client.tls_set()
client.on_connect, client.on_subscribe, client.on_message = on_connect, on_subscribe, on_message
client.connect(HOST, 8883, keepalive=30)
client.loop_start()
ok = got.wait(timeout=15) and not errors
for e in errors:
    print(e)
client.loop_stop()
client.disconnect()
print("smoke test passed" if ok else "smoke test FAILED: no echo within 15 s")
sys.exit(0 if ok else 1)
