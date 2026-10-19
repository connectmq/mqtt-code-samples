import ssl
import time
import uuid

import paho.mqtt.client as mqtt

BROKER = "broker.connectmq.com"
PORT = 8883
TOPIC = "connectmq/demo/k7f3q2/secure"


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Connect failed: {reason_code}")
        return
    sock = client.socket()
    print(f"Connected over {sock.version()} using {sock.cipher()[0]}")
    client.subscribe(TOPIC, qos=1)


def on_message(client, userdata, msg):
    print(f"{msg.topic}: {msg.payload.decode()}")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=f"tls-{uuid.uuid4().hex[:8]}")
client.on_connect = on_connect
client.on_message = on_message

# Use the operating system's trusted CAs, require a valid certificate,
# and verify that it matches BROKER. This is the secure default.
client.tls_set(cert_reqs=ssl.CERT_REQUIRED, tls_version=ssl.PROTOCOL_TLS_CLIENT)

client.connect(BROKER, PORT, keepalive=60)
client.loop_start()
time.sleep(2)
client.publish(TOPIC, "hello over TLS", qos=1)
time.sleep(2)
client.disconnect()
client.loop_stop()
