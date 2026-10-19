# Subscribe to the temperature topic (TLS: the system CA store verifies the broker certificate)
mosquitto_sub -h YOUR_BROKER_HOST -p 8883 --capath /etc/ssl/certs \
  -u YOUR_USERNAME -P YOUR_PASSWORD -t "your-project/sensors/#" -v

# Publish a JSON reading
mosquitto_pub -h YOUR_BROKER_HOST -p 8883 --capath /etc/ssl/certs \
  -u YOUR_USERNAME -P YOUR_PASSWORD -t "your-project/sensors/temperature" -m '{"temperature":21.5}'
