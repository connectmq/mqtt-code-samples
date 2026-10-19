# probe.py  (pip install paho-mqtt)
import json, os, statistics, time, uuid
import paho.mqtt.client as mqtt

HOST, PORT = os.environ.get("MQTT_HOST", "YOUR_BROKER_HOST"), 8883
USER, PASS = os.environ.get("MQTT_USER", "YOUR_USERNAME"), os.environ.get("MQTT_PASS", "YOUR_PASSWORD")
TOPIC = f"loadtest/probe/{uuid.uuid4().hex[:6]}"
COUNT, INTERVAL = 600, 0.5

latencies, seen = [], set()

def on_message(client, userdata, msg):
    data = json.loads(msg.payload)
    latencies.append((time.time() - data["ts"]) * 1000)
    seen.add(data["seq"])

def make(name):
    c = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=f"probe-{name}-{uuid.uuid4().hex[:6]}")
    c.username_pw_set(USER, PASS)
    c.tls_set()
    c.connect(HOST, PORT, keepalive=30)
    c.loop_start()
    return c

sub = make("sub")
sub.on_message = on_message
sub.subscribe(TOPIC, qos=1)
time.sleep(1)
pub = make("pub")

for seq in range(COUNT):
    pub.publish(TOPIC, json.dumps({"seq": seq, "ts": time.time()}), qos=1)
    time.sleep(INTERVAL)

time.sleep(5)
q = statistics.quantiles(latencies, n=100)
print(f"received {len(seen)}/{COUNT}, lost {COUNT - len(seen)}")
print(f"latency ms p50={q[49]:.1f} p95={q[94]:.1f} p99={q[98]:.1f} max={max(latencies):.1f}")
