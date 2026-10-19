# --- Generate a random ID (client ID base and topic prefix) ---
export ID=demo-$(openssl rand -hex 3)
echo $ID   # e.g. demo-7f3a91

# --- Terminal 1: subscribe to your prefix ---
mosquitto_sub -h broker.connectmq.com -p 1883 -i $ID-sub -t "connectmq/demo/$ID/#" -v

# --- Terminal 2: publish a message ---
mosquitto_pub -h broker.connectmq.com -p 1883 -i $ID-pub -t "connectmq/demo/$ID/temperature" -m '{"value": 22.5, "unit": "C"}'

# --- Publish over TLS (port 8883) with the system CA bundle, MQTT 5.0 ---
mosquitto_pub -h broker.connectmq.com -p 8883 --capath /etc/ssl/certs -i $ID-tls -t "connectmq/demo/$ID/tls" -m "hello over TLS" -V mqttv5

# --- Retained message demo ---
# Publish a retained status
mosquitto_pub -h broker.connectmq.com -p 1883 -i $ID-pub -t "connectmq/demo/$ID/status" -m "online" -r -q 1

# A brand-new subscriber receives it instantly, even though it was published earlier
mosquitto_sub -h broker.connectmq.com -p 1883 -i $ID-late -t "connectmq/demo/$ID/status" -v -C 1 -W 5

# Clear the retained message by publishing an empty retained payload
mosquitto_pub -h broker.connectmq.com -p 1883 -i $ID-pub -t "connectmq/demo/$ID/status" -n -r

# --- Last Will and Testament demo ---
# Start a "device" with a will, then kill the terminal/process (not a clean Ctrl+C)
mosquitto_sub -h broker.connectmq.com -p 1883 -i $ID-device -t "connectmq/demo/$ID/cmd" -k 5 --will-topic "connectmq/demo/$ID/status" --will-payload "offline" --will-qos 1
