import uuid
import paho.mqtt.client as mqtt

TOPIC = "connectmq/demo/k3x8p1/libs/python"

def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected:", reason_code)
    client.subscribe(TOPIC, qos=1)
    client.publish(TOPIC, "hello from paho-mqtt", qos=1)

def on_message(client, userdata, msg):
    print(msg.topic, msg.payload.decode())

client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id=f"libs-py-{uuid.uuid4().hex[:8]}",
    protocol=mqtt.MQTTv5,
)
client.on_connect = on_connect
client.on_message = on_message
client.tls_set()
client.connect("broker.connectmq.com", 8883, keepalive=30)
client.loop_forever()
