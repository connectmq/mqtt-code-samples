#!/usr/bin/env bash
# MQTT CLI tools compared, from https://connectmq.com/blog/mqtt-cli-tools/
# This is a reference sheet: copy the commands you need into a terminal one at a time
# (subscribers keep running until you press Ctrl+C). Replace c1t9 with your own random string.

# --- mosquitto_pub and mosquitto_sub ---
mosquitto_sub -h broker.connectmq.com -p 1883 -i cli-cmp-sub1 -t 'connectmq/demo/c1t9/#' -v
mosquitto_pub -h broker.connectmq.com -p 1883 -i cli-cmp-pub1 -t connectmq/demo/c1t9/test -m 'hello' -q 1

# Health check in a script: fail if no reading within 10 seconds
if ! mosquitto_sub -h broker.connectmq.com -p 1883 -i health-c1t9 \
     -t connectmq/demo/c1t9/sensor/temp -C 1 -W 10 > /dev/null; then
  echo "sensor silent" >&2; exit 1
fi

# --- MQTTX CLI ---
mqttx sub -h broker.connectmq.com -p 1883 -i cli-cmp-sub2 -t 'connectmq/demo/c1t9/#' -v
mqttx pub -h broker.connectmq.com -p 1883 -i cli-cmp-pub2 -t connectmq/demo/c1t9/test -m 'hello' -q 1
mqttx conn -h broker.connectmq.com -p 8883 -l mqtts -i cli-cmp-conn2

# --- HiveMQ MQTT CLI ---
mqtt sub -h broker.connectmq.com -p 1883 -i cli-cmp-sub3 -t 'connectmq/demo/c1t9/#'
mqtt pub -h broker.connectmq.com -p 1883 -i cli-cmp-pub3 -t connectmq/demo/c1t9/test -m 'hello' -q 1

# Interactive shell
mqtt shell
# Inside the shell: con -h broker.connectmq.com -i cli-cmp-shell3

# --- MQTT.js CLI ---
npm install -g mqtt
mqtt sub -h broker.connectmq.com -p 1883 -i cli-cmp-sub4 -t 'connectmq/demo/c1t9/#' -v
mqtt pub -h broker.connectmq.com -p 1883 -i cli-cmp-pub4 -t connectmq/demo/c1t9/test -m 'hello'

# --- curl ---
# Subscribe (prints raw payloads; Ctrl+C to stop)
curl -s mqtt://broker.connectmq.com:1883/connectmq%2Fdemo%2Fc1t9%2Ftest

# Publish
curl -d 'hello from curl' mqtt://broker.connectmq.com:1883/connectmq%2Fdemo%2Fc1t9%2Ftest

# --- mqttui ---
mqttui --broker mqtt://broker.connectmq.com:1883 'connectmq/demo/c1t9/#'

# --- The same test in every tool: receive and exit (one message or timeout) ---
mosquitto_sub -h broker.connectmq.com -i s1-c1t9 -t 'connectmq/demo/c1t9/#' -C 1
timeout 10 mqttx sub -h broker.connectmq.com -i s2-c1t9 -t 'connectmq/demo/c1t9/#'
timeout 10 mqtt sub -h broker.connectmq.com -i s3-c1t9 -t 'connectmq/demo/c1t9/#'   # HiveMQ CLI
timeout 10 mqtt sub -h broker.connectmq.com -i s4-c1t9 -t 'connectmq/demo/c1t9/#'   # MQTT.js CLI
timeout 5 curl -s mqtt://broker.connectmq.com/connectmq%2Fdemo%2Fc1t9%2Ftest

# --- Private broker (TLS + credentials) ---
mosquitto_sub -h YOUR_BROKER_HOST -p 8883 --capath /etc/ssl/certs \
  -i YOUR_CLIENT_ID -u YOUR_USERNAME -P YOUR_PASSWORD -t '#' -v
