# Type-Safe MQTT TypeScript Client: Typed Topics and Validated Payloads

[![ConnectMQ](https://img.shields.io/badge/MQTT%20broker-ConnectMQ-84cc16)](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-typescript-badge)
[![Free public broker](https://img.shields.io/badge/public%20broker-broker.connectmq.com-0b2545)](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-typescript-badge)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](../../LICENSE)

Define a single contract file for topics, QoS and payload schemas, wrap MQTT.js in a typed client, and validate every incoming message at runtime so publishers and subscribers can never drift apart.

> **Built for [ConnectMQ](https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-typescript-intro)** — the managed, serverless MQTT broker for IoT. Run this tutorial on the free public broker `broker.connectmq.com` without an account, then move the same code to a secure private broker with a free ConnectMQ account. 👉 [Start for free](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-typescript-intro)

📖 **Full step-by-step tutorial:** [Type-Safe MQTT TypeScript Client: Typed Topics and Validated Payloads](https://connectmq.com/blog/mqtt-typescript/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-typescript-intro)

<p align="center"><a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-typescript-hero"><img src="../../assets/connectmq-website.png" alt="ConnectMQ — managed MQTT broker: connect sensors, PLC gateways, vehicles and smart homes to dashboards, backends, mobile apps and data platforms" width="820"></a></p>

## What's inside

| File | What it does |
| --- | --- |
| [`src/contracts.ts`](src/contracts.ts) | Single source of truth: topic filters, typed topic builders, QoS, retain flags and zod payload schemas |
| [`src/typed-client.ts`](src/typed-client.ts) | `TypedMqttClient`, a typed MQTT.js wrapper that validates outgoing and incoming payloads and restores subscriptions on reconnect |
| [`src/demo.ts`](src/demo.ts) | Demo that subscribes to telemetry and commands and publishes status, telemetry and a reboot command |
| [`package.json`](package.json) | ES module project with `mqtt`, `zod`, `typescript`, `tsx` and `@types/node` |

## Requirements

- Node.js with npm
- [MQTT.js](https://github.com/mqttjs/MQTT.js) v5 (ships its own TypeScript types)
- [zod](https://zod.dev/) for schemas
- TypeScript, `tsx` and `@types/node` as dev dependencies
- Optional: `mosquitto_pub` to send a broken payload

## Run it on the free public broker

1. Install the dependencies and create a strict `tsconfig.json` (as in the post):

   ```bash
   npm install mqtt zod
   npm install -D typescript tsx @types/node
   npx tsc --init --strict --target es2022 --module nodenext --moduleResolution nodenext
   ```

   Starting from scratch, the post's full setup is:

   ```bash
   mkdir mqtt-typescript-demo && cd mqtt-typescript-demo
   npm init -y
   npm pkg set type=module
   npm install mqtt zod
   npm install -D typescript tsx @types/node
   npx tsc --init --strict --target es2022 --module nodenext --moduleResolution nodenext
   ```

2. Change the topic prefix `ts-7f3a` to your own random string (or set `TOPIC_PREFIX`), then run the demo and type-check separately:

   ```bash
   npx tsx src/demo.ts
   npx tsc --noEmit
   ```

   Uncomment the two "do not compile" lines in `src/demo.ts` and `tsc` reports the errors.

3. See runtime validation in action by publishing a broken payload:

   ```bash
   mosquitto_pub -h broker.connectmq.com -p 1883 -i ts-bad-7f3a \
     -t connectmq/demo/ts-7f3a/devices/sensor-9/telemetry -m '{"deviceId":"sensor-9","temperature":"hot"}'
   ```

   The demo logs an `Invalid payload` warning and your handler is never called.

> ⚠️ **The public broker is shared:** anyone can subscribe to any topic. Use a unique topic prefix and never send passwords or personal data. [About the free public MQTT broker](https://connectmq.com/public-mqtt-broker/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-typescript-private)

## Run it on your private ConnectMQ broker

For real devices, switch to a private broker: TLS, a username and password per device and per-topic access control.

1. [Create a free ConnectMQ account](https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-typescript-private) — the **Serverless (Free)** plan needs no credit card.
2. Create a broker in the dashboard and copy its **host**, **username** and **password**.
3. Only the constructor in `src/demo.ts` changes. Replace it with the post's private-broker version and set `MQTT_HOST`, `MQTT_CLIENT_ID`, `MQTT_USERNAME` and `MQTT_PASSWORD` as environment variables:

   ```typescript
   const mq = new TypedMqttClient(`mqtts://${process.env.MQTT_HOST}:8883`, {
     clientId: process.env.MQTT_CLIENT_ID!,   // YOUR_CLIENT_ID
     username: process.env.MQTT_USERNAME!,    // YOUR_USERNAME
     password: process.env.MQTT_PASSWORD!,    // YOUR_PASSWORD
   });
   ```

What you get with a private broker:

- 🔒 **TLS encryption** on every connection (port 8883, secure WebSocket 8084)
- 🔑 **A username and password per device**, created in the dashboard
- 🛡️ **Per-topic access control (ACL)** — decide which client may publish or subscribe to which topic
- 📊 **Live dashboard** — device status, last values, rules, alerts and a 3D digital twin

## Related

- 📖 [Type-Safe MQTT TypeScript Client: Typed Topics and Validated Payloads](https://connectmq.com/blog/mqtt-typescript/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-typescript-related) — the full tutorial with explanations
- 🧩 [Node.js basic example](../../nodejs/)
- 🗂️ [All tutorials](../) · [All code samples](../../)

---

<p align="center">
  <a href="https://connectmq.com/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-typescript-footer"><b>ConnectMQ</b></a> — managed MQTT broker for IoT ·
  <a href="https://app.connectmq.com/signup?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-typescript-footer">Start for free</a> ·
  <a href="https://connectmq.com/pricing/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-typescript-footer">Pricing</a> ·
  <a href="https://connectmq.com/blog/?utm_source=github&utm_medium=code-samples&utm_campaign=mqtt-code-samples&utm_content=tut-mqtt-typescript-footer">Blog</a>
</p>
