import json
import paho.mqtt.client as mqtt

TOPIC = "your-project/sensors/temperature"  # Use a unique topic prefix: everyone can read the public broker

# Runs when the connection is established
def on_connect(client, userdata, flags, reason_code, properties):
    print("Connected:", reason_code)
    # Subscribe to the temperature topic
    client.subscribe(TOPIC, qos=1)
    # Publish a JSON reading
    client.publish(TOPIC, json.dumps({"temperature": 21.5}), qos=1)

# Runs for every message on a subscribed topic
def on_message(client, userdata, msg):
    print(msg.topic, msg.payload.decode())

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

# Connect to the free public broker (no account needed)
client.connect("broker.connectmq.com", 1883)
# Keep the client running
client.loop_forever()
