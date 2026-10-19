#!/usr/bin/env bash
# mosquitto_pub / mosquitto_sub examples from
# https://connectmq.com/blog/mosquitto-pub-mosquitto-sub-examples/
# This is a reference sheet: copy the commands you need into a terminal one at a time
# (many of them keep running until you press Ctrl+C). Replace x7q2 with your own random string.

# --- Install the Mosquitto clients ---
# Debian / Ubuntu / Raspberry Pi OS
sudo apt install mosquitto-clients

# macOS
brew install mosquitto

# Windows: install Mosquitto from mosquitto.org; the installer includes mosquitto_pub.exe and mosquitto_sub.exe

# --- Shell variables (bash/zsh) ---
H="-h broker.connectmq.com -p 1883"
T="connectmq/demo/x7q2"

# --- Basic examples ---
# 1. Subscribe to one topic
mosquitto_sub $H -i sub-x7q2 -t "$T/hello"

# 2. Publish a message
mosquitto_pub $H -i pub-x7q2 -t "$T/hello" -m "hello from the CLI"

# 3. Subscribe to everything under your prefix and print topics
mosquitto_sub $H -i sub-x7q2 -t "$T/#" -v

# 4. Single-level wildcard: all temperature topics, any room
mosquitto_sub $H -i sub-x7q2 -t "$T/+/temperature" -v

# 5. Several topic filters in one client
mosquitto_sub $H -i sub-x7q2 -t "$T/+/temperature" -t "$T/+/humidity" -v

# 6. Publish JSON
mosquitto_pub $H -i pub-x7q2 -t "$T/kitchen/temperature" -m '{"value": 21.8, "unit": "C"}'

# --- QoS and sessions ---
# 7. Publish and subscribe with QoS 1
mosquitto_sub $H -i sub-x7q2 -t "$T/alarms" -q 1 -v
mosquitto_pub $H -i pub-x7q2 -t "$T/alarms" -q 1 -m "door open"

# 8. Watch the protocol exchange with -d
mosquitto_pub $H -i pub-x7q2 -t "$T/alarms" -q 2 -m "test" -d

# 9. Persistent session: receive messages published while you were offline
# Subscribe once with a fixed ID, clean session disabled, then Ctrl+C
mosquitto_sub $H -i sub-persist-x7q2 -c -q 1 -t "$T/queue" -v
# While it is stopped, publish at QoS 1
mosquitto_pub $H -i pub-x7q2 -q 1 -t "$T/queue" -m "queued while offline"
# Reconnect with the same ID and -c: the message is delivered
mosquitto_sub $H -i sub-persist-x7q2 -c -q 1 -t "$T/queue" -v

# 10. MQTT 5 session expiry (keep the session for 300 seconds after disconnect)
mosquitto_sub $H -V 5 -i sub-persist-x7q2 -c -x 300 -q 1 -t "$T/queue" -v

# --- Retained messages ---
# 11. Publish a retained state
mosquitto_pub $H -i pub-x7q2 -t "$T/pump1/state" -r -m "running"

# 12. Show only retained messages, then exit
mosquitto_sub $H -i sub-x7q2 -t "$T/#" -v --retained-only -W 3

# 13. Ignore old retained messages
mosquitto_sub $H -i sub-x7q2 -t "$T/#" -v -R

# 14. Delete a retained message (publish an empty retained payload)
mosquitto_pub $H -i pub-x7q2 -t "$T/pump1/state" -r -n

# 15. Clear every retained message under your prefix
mosquitto_sub $H -i cleaner-x7q2 -t "$T/#" --remove-retained --retained-only -W 3

# --- Last Will and Testament ---
# 16. Register a Last Will that marks the client offline
mosquitto_sub $H -i device-x7q2 -t "$T/device1/cmd" \
  --will-topic "$T/device1/status" --will-payload "offline" --will-retain --will-qos 1
# In another terminal, watch status:
mosquitto_sub $H -i watch-x7q2 -t "$T/device1/status" -v

# --- Scripting and output control ---
# 17. Receive exactly N messages, then exit
mosquitto_sub $H -i sub-x7q2 -t "$T/kitchen/temperature" -C 1

# 18. Custom output format with timestamps
mosquitto_sub $H -i sub-x7q2 -t "$T/#" -F "@Y-@m-@dT@H:@M:@S %t %p"

# 19. JSON output for piping into jq
mosquitto_sub $H -i sub-x7q2 -t "$T/#" -F "%j" | jq -c '{topic, payload}'

# 20. Publish each line of a file or stdin as a separate message
printf '20.1\n20.4\n20.9\n' | mosquitto_pub $H -i pub-x7q2 -t "$T/kitchen/temperature" -l

# 21. A tiny sensor simulator (respect the public limit of 10 messages per second per client)
while true; do
  mosquitto_pub $H -i sim-x7q2 -t "$T/lab/temperature" \
    -m "{\"value\": $((RANDOM % 10 + 20)), \"ts\": $(date +%s)}"
  sleep 1
done

# --- TLS and authentication ---
# 22. Encrypted connection on port 8883
# Linux: use the system CA bundle
mosquitto_sub -h broker.connectmq.com -p 8883 --capath /etc/ssl/certs \
  -i tls-x7q2 -t "$T/#" -v

# 23. Private broker with credentials
mosquitto_pub -h YOUR_BROKER_HOST -p 8883 --capath /etc/ssl/certs \
  -i YOUR_CLIENT_ID -u YOUR_USERNAME -P YOUR_PASSWORD \
  -t "factory1/line1/cnc1/telemetry" -q 1 -m '{"spindle_rpm": 8000}'

# --- MQTT 5 properties ---
# 24. Content type, user property and message expiry
mosquitto_pub $H -V 5 -i pub-x7q2 -t "$T/kitchen/temperature" -m '{"value": 22}' \
  -D PUBLISH content-type application/json \
  -D PUBLISH user-property source cli-test \
  -D PUBLISH message-expiry-interval 60

# 25. Request/response with mosquitto_rr
# Responder: read the response topic (%R) of each request and answer it
while true; do
  RT=$(mosquitto_sub $H -V 5 -i resp-x7q2 -t "$T/rpc/time" -C 1 -F "%R")
  mosquitto_pub $H -V 5 -i resp-pub-x7q2 -t "$RT" -m "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
done &

# Requester: sets the response topic, waits for one reply and prints it
mosquitto_rr $H -V 5 -i req-x7q2 -t "$T/rpc/time" -e "$T/rpc/time/reply" -m "now?" -W 5
