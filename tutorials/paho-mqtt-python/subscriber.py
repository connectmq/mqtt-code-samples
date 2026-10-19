import uuid

import paho.mqtt.client as mqtt

BROKER = "broker.connectmq.com"
PORT = 1883
TOPIC = "connectmq/demo/k7f3q2/#"


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"Connection failed: {reason_code}")
        return
    print(f"Connected to {BROKER}")
    # Subscribe here so the subscription is restored after every reconnect.
    client.subscribe(TOPIC, qos=1)


def on_subscribe(client, userdata, mid, reason_code_list, properties):
    for rc in reason_code_list:
        if rc.is_failure:
            print(f"Subscription rejected: {rc}")
        else:
            print(f"Subscribed with QoS {rc.value}")


def on_message(client, userdata, msg):
    retained = " (retained)" if msg.retain else ""
    print(f"{msg.topic}{retained}: {msg.payload.decode('utf-8', errors='replace')}")


def on_disconnect(client, userdata, disconnect_flags, reason_code, properties):
    print(f"Disconnected: {reason_code}")


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=f"sub-{uuid.uuid4().hex[:8]}")
client.on_connect = on_connect
client.on_subscribe = on_subscribe
client.on_message = on_message
client.on_disconnect = on_disconnect

client.connect(BROKER, PORT, keepalive=60)
client.loop_forever()
