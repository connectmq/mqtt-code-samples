import time
import uuid

import paho.mqtt.client as mqtt

BROKER = "broker.connectmq.com"
PREFIX = "connectmq/demo/k7f3q2"


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Connect failed: {reason_code}")
        return
    print(f"Connected (session present: {flags.session_present})")
    client.subscribe(f"{PREFIX}/#", qos=1)


def on_subscribe(client, userdata, mid, reason_code_list, properties):
    for rc in reason_code_list:
        print("Subscribe rejected:" if rc.is_failure else "Granted QoS:", rc)


def on_publish(client, userdata, mid, reason_code, properties):
    print(f"Publish {mid} acknowledged: {reason_code}")


def on_message(client, userdata, msg):
    print(f"{msg.topic}: {msg.payload.decode()}")


def on_disconnect(client, userdata, disconnect_flags, reason_code, properties):
    print(f"Disconnected: {reason_code}")


client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id=f"migrate-{uuid.uuid4().hex[:8]}",
    protocol=mqtt.MQTTv5,
)
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_publish = on_publish
client.on_message = on_message
client.on_disconnect = on_disconnect

client.connect(BROKER, 1883, keepalive=60)
client.loop_start()
time.sleep(1)

for i in range(3):
    client.publish(f"{PREFIX}/test", f"hello {i}", qos=1)
    time.sleep(1)

client.disconnect()
client.loop_stop()
