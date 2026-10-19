import json
import ssl
import uuid
import paho.mqtt.client as mqtt

DEVICE_ID = f"demo-{uuid.uuid4().hex[:6]}"
PREFIX = f"connectmq/demo/{DEVICE_ID}"

def on_connect(client, userdata, flags, reason_code, properties):
    print(f"Connected: {reason_code}")
    client.subscribe(f"{PREFIX}/#", qos=1)
    client.publish(f"{PREFIX}/temperature", json.dumps({"value": 21.8}), qos=1)

def on_message(client, userdata, msg):
    print(f"{msg.topic} -> {msg.payload.decode()}")

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id=DEVICE_ID,
    protocol=mqtt.MQTTv5,
)
client.tls_set(cert_reqs=ssl.CERT_REQUIRED)  # uses the system CA store
client.on_connect = on_connect
client.on_message = on_message

client.connect("broker.connectmq.com", 8883, keepalive=30)
client.loop_forever()
