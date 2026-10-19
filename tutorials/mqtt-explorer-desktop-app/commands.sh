#!/usr/bin/env bash
# Seed a topic tree to compare MQTT explorer desktop apps, from
# https://connectmq.com/blog/mqtt-explorer-desktop-app/
# Replace ex4m with your own random string; the public area is visible to everyone.

# --- Seed a retained topic tree ---
P="connectmq/demo/ex4m"
H="-h broker.connectmq.com -p 1883 -i seed-ex4m"

mosquitto_pub $H -r -t "$P/plant1/line1/cnc1/status"      -m "running"
mosquitto_pub $H -r -t "$P/plant1/line1/cnc1/telemetry"   -m '{"spindle_rpm": 8200, "temp_c": 41.5}'
mosquitto_pub $H -r -t "$P/plant1/line1/robot1/status"    -m "idle"
mosquitto_pub $H -r -t "$P/plant1/line2/furnace1/telemetry" -m '{"temp_c": 812, "setpoint_c": 820}'
mosquitto_pub $H -r -t "$P/plant1/utilities/tank1/level"  -m "67.2"

# --- Add a live, changing value so history and charts have something to show ---
for i in $(seq 1 60); do
  mosquitto_pub -h broker.connectmq.com -p 1883 -i seed-live-ex4m \
    -t "connectmq/demo/ex4m/plant1/utilities/tank1/level" -m "$((60 + RANDOM % 15)).$((RANDOM % 10))"
  sleep 1
done
