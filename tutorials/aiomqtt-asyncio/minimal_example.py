import asyncio
import sys
import uuid

import aiomqtt

BROKER = "broker.connectmq.com"
PREFIX = "connectmq/demo/k7f3q2"


async def main():
    async with aiomqtt.Client(BROKER, 1883, identifier=f"aio-{uuid.uuid4().hex[:8]}") as client:
        await client.subscribe(f"{PREFIX}/hello", qos=1)
        await client.publish(f"{PREFIX}/hello", payload="hello from asyncio", qos=1)
        async for message in client.messages:
            print(message.topic, message.payload.decode())
            break  # stop after the first message


if sys.platform == "win32":
    asyncio.run(main(), loop_factory=asyncio.SelectorEventLoop)
else:
    asyncio.run(main())
