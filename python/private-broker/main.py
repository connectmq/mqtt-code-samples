import json
import paho.mqtt.client as mqtt

TOPIC = "your-project/sensors/temperature"

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

# Username and password from your ConnectMQ dashboard
client.username_pw_set("YOUR_USERNAME", "YOUR_PASSWORD")
# TLS: the system CA store verifies the broker certificate
client.tls_set()

# Connect to your private ConnectMQ broker on port 8883
client.connect("YOUR_BROKER_HOST", 8883)
# Keep the client running
client.loop_forever()
