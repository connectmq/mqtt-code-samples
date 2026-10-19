import json
import os
import threading
import time
import uuid

import paho.mqtt.client as mqtt
import requests

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
ALLOWED_CHATS = {int(c) for c in os.environ["TELEGRAM_CHAT_IDS"].split(",")}
API = f"https://api.telegram.org/bot{BOT_TOKEN}"

BROKER = os.environ.get("MQTT_HOST", "broker.connectmq.com")
PORT = int(os.environ.get("MQTT_PORT", "1883"))
USERNAME = os.environ.get("MQTT_USERNAME")
PASSWORD = os.environ.get("MQTT_PASSWORD")
CLIENT_ID = os.environ.get("MQTT_CLIENT_ID", f"tgbot-{uuid.uuid4().hex[:8]}")
PREFIX = os.environ.get("TOPIC_PREFIX", "connectmq/demo/tgbot-9214")
ALERT_COOLDOWN = int(os.environ.get("ALERT_COOLDOWN", "300"))  # seconds per device

latest = {}            # device -> (timestamp, payload dict)
last_alert = {}        # device -> timestamp of last forwarded alert
state_lock = threading.Lock()


def send(chat_id: int, text: str):
    try:
        r = requests.post(f"{API}/sendMessage", json={"chat_id": chat_id, "text": text}, timeout=10)
        if r.status_code == 429:
            retry = r.json().get("parameters", {}).get("retry_after", 5)
            time.sleep(retry)
            requests.post(f"{API}/sendMessage", json={"chat_id": chat_id, "text": text}, timeout=10)
    except requests.RequestException as exc:
        print(f"Telegram send failed: {exc}")


def broadcast(text: str):
    for chat_id in ALLOWED_CHATS:
        send(chat_id, text)


# ---------- MQTT side ----------

def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code.is_failure:
        print(f"MQTT connect failed: {reason_code}")
        return
    client.subscribe(f"{PREFIX}/+/telemetry", qos=0)
    client.subscribe(f"{PREFIX}/+/alert", qos=1)
    print("MQTT connected and subscribed")


def on_message(client, userdata, msg):
    parts = msg.topic.split("/")
    device, kind = parts[-2], parts[-1]
    try:
        payload = json.loads(msg.payload)
    except (json.JSONDecodeError, UnicodeDecodeError):
        payload = {"raw": msg.payload.decode("utf-8", errors="replace")}

    now = time.time()
    if kind == "telemetry":
        with state_lock:
            latest[device] = (now, payload)
    elif kind == "alert" and not msg.retain:
        with state_lock:
            if now - last_alert.get(device, 0) < ALERT_COOLDOWN:
                return
            last_alert[device] = now
        level = str(payload.get("level", "alert")).upper()
        text = payload.get("text", json.dumps(payload))
        # send from a separate thread so a slow HTTP call never blocks the MQTT loop
        threading.Thread(target=broadcast, args=(f"[{level}] {device}: {text}",), daemon=True).start()


# ---------- Telegram side ----------

def handle_command(client: mqtt.Client, chat_id: int, text: str):
    parts = text.strip().split()
    cmd = parts[0].split("@")[0].lower()
    arg = parts[1] if len(parts) > 1 else None

    if cmd in ("/start", "/help"):
        send(chat_id, "Commands:\n/status - latest values\n/on <device>\n/off <device>")
    elif cmd == "/status":
        with state_lock:
            snapshot = dict(latest)
        if not snapshot:
            send(chat_id, "No telemetry received yet.")
            return
        lines = []
        for device, (ts, data) in sorted(snapshot.items()):
            age = int(time.time() - ts)
            lines.append(f"{device}: {json.dumps(data)} ({age}s ago)")
        send(chat_id, "\n".join(lines))
    elif cmd in ("/on", "/off"):
        if not arg or "/" in arg or "+" in arg or "#" in arg:
            send(chat_id, f"Usage: {cmd} <device>")
            return
        body = json.dumps({"action": cmd[1:], "by": f"telegram:{chat_id}"})
        info = client.publish(f"{PREFIX}/{arg}/cmd", body, qos=1)
        info.wait_for_publish(timeout=5)
        send(chat_id, f"Sent '{cmd[1:]}' to {arg}" if info.is_published() else "Publish failed, broker not reachable")
    else:
        send(chat_id, "Unknown command. Try /help")


def poll_telegram(client: mqtt.Client):
    offset = None
    while True:
        try:
            r = requests.get(f"{API}/getUpdates", params={"timeout": 30, "offset": offset}, timeout=40)
            for update in r.json().get("result", []):
                offset = update["update_id"] + 1
                message = update.get("message") or {}
                chat_id = message.get("chat", {}).get("id")
                text = message.get("text", "")
                if chat_id not in ALLOWED_CHATS:
                    print(f"Ignoring chat {chat_id}")
                    continue
                if text.startswith("/"):
                    handle_command(client, chat_id, text)
        except requests.RequestException as exc:
            print(f"Telegram polling error: {exc}")
            time.sleep(5)


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=CLIENT_ID)
    if USERNAME:
        client.username_pw_set(USERNAME, PASSWORD)
    if PORT == 8883:
        client.tls_set()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, keepalive=60)
    client.loop_start()
    broadcast("Bot started")
    poll_telegram(client)


if __name__ == "__main__":
    main()
