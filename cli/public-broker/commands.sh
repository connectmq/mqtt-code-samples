# Subscribe to the temperature topic
mosquitto_sub -h broker.connectmq.com -p 1883 -t "your-project/sensors/#" -v

# Publish a JSON reading
mosquitto_pub -h broker.connectmq.com -p 1883 -t "your-project/sensors/temperature" -m '{"temperature":21.5}'
