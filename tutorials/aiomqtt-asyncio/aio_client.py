import asyncio
import json
import random
import sys
import time
import uuid

import aiomqtt

BROKER = "broker.connectmq.com"
PORT = 1883
PREFIX = "connectmq/demo/k7f3q2"
CLIENT_ID = f"aio-{uuid.uuid4().hex[:8]}"
RECONNECT_INTERVAL = 5
WORKERS = 3


async def publish_readings(client: aiomqtt.Client) -> None:
    seq = 0
    while True:
        reading = {"seq": seq, "temperature": round(random.uniform(20, 25), 2), "ts": time.time()}
        await client.publish(f"{PREFIX}/sensors/room1", json.dumps(reading), qos=1)
        seq += 1
        await asyncio.sleep(2)


async def consume(client: aiomqtt.Client, queue: asyncio.Queue) -> None:
    await client.subscribe(f"{PREFIX}/sensors/+", qos=1)
    await client.subscribe(f"{PREFIX}/commands/#", qos=1)
    async for message in client.messages:
        await queue.put(message)  # hand off quickly, keep reading


async def handle(message: aiomqtt.Message) -> None:
    if message.topic.matches(f"{PREFIX}/commands/#"):
        print(f"Command on {message.topic}: {message.payload.decode()}")
        return
    data = json.loads(message.payload)
    await asyncio.sleep(0.5)  # stands in for a slow database or HTTP call
    print(f"Processed reading {data['seq']}: {data['temperature']} C")


async def worker(name: int, queue: asyncio.Queue) -> None:
    while True:
        message = await queue.get()
        try:
            await handle(message)
        except Exception as exc:  # one bad message must not kill the worker
            print(f"Worker {name} failed on {message.topic}: {exc}")
        finally:
            queue.task_done()


async def main() -> None:
    queue: asyncio.Queue = asyncio.Queue(maxsize=1000)
    workers = [asyncio.create_task(worker(i, queue)) for i in range(WORKERS)]

    client = aiomqtt.Client(
        BROKER,
        PORT,
        identifier=CLIENT_ID,
        protocol=aiomqtt.ProtocolVersion.V5,
        keepalive=30,
        will=aiomqtt.Will(f"{PREFIX}/status/{CLIENT_ID}", payload="offline", qos=1, retain=True),
        # Private ConnectMQ broker:
        # username="YOUR_USERNAME", password="YOUR_PASSWORD",
        # tls_context=ssl.create_default_context(), and port 8883
    )

    try:
        while True:
            try:
                async with client:
                    print("Connected")
                    await client.publish(f"{PREFIX}/status/{CLIENT_ID}", "online", qos=1, retain=True)
                    async with asyncio.TaskGroup() as tg:
                        tg.create_task(publish_readings(client))
                        tg.create_task(consume(client, queue))
            except* aiomqtt.MqttError as group:
                print(f"Connection lost: {group.exceptions[0]}. Reconnecting in {RECONNECT_INTERVAL}s")
            await asyncio.sleep(RECONNECT_INTERVAL)
    finally:
        for w in workers:
            w.cancel()


if __name__ == "__main__":
    try:
        if sys.platform == "win32":
            asyncio.run(main(), loop_factory=asyncio.SelectorEventLoop)
        else:
            asyncio.run(main())
    except KeyboardInterrupt:
        print("Stopped")
