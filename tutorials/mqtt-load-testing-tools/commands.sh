#!/usr/bin/env bash
# MQTT load testing commands from the tutorial.
# Run these ONLY against your own private broker, never against the shared public broker.

# --- emqtt-bench ---------------------------------------------------------

# Ramp up 500 connections, one every 10 ms
emqtt_bench conn -h YOUR_BROKER_HOST -p 1883 -c 500 -i 10 \
  -u YOUR_USERNAME -P YOUR_PASSWORD

# 50 subscribers on a wildcard, QoS 1
emqtt_bench sub -h YOUR_BROKER_HOST -p 1883 -c 50 -i 10 \
  -t 'loadtest/#' -q 1 -u YOUR_USERNAME -P YOUR_PASSWORD

# 200 publishers, each sending a 256-byte message every 1000 ms to its own topic
emqtt_bench pub -h YOUR_BROKER_HOST -p 1883 -c 200 -i 10 -I 1000 \
  -t 'loadtest/device/%i' -s 256 -q 1 -u YOUR_USERNAME -P YOUR_PASSWORD

# --- MQTTX Bench ---------------------------------------------------------

mqttx bench conn -c 200 -i 10 -h YOUR_BROKER_HOST -p 8883 -l mqtts \
  -u YOUR_USERNAME -P YOUR_PASSWORD

mqttx bench sub -c 20 -t 'loadtest/#' -q 1 -h YOUR_BROKER_HOST -p 8883 -l mqtts \
  -u YOUR_USERNAME -P YOUR_PASSWORD

mqttx bench pub -c 100 -i 10 -im 1000 -t 'loadtest/device/%i' -q 1 \
  -m '{"temp": 21.5}' -h YOUR_BROKER_HOST -p 8883 -l mqtts \
  -u YOUR_USERNAME -P YOUR_PASSWORD

# --- Locust --------------------------------------------------------------

locust -f locustfile.py --headless -u 100 -r 5 --run-time 10m
