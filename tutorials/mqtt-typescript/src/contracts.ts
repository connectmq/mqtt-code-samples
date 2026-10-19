import { z } from "zod";

export const PREFIX = process.env.TOPIC_PREFIX ?? "connectmq/demo/ts-7f3a";

export const Telemetry = z.object({
  deviceId: z.string(),
  temperature: z.number(),
  humidity: z.number().min(0).max(100),
  ts: z.number().int(),
});

export const Command = z.object({
  action: z.enum(["on", "off", "reboot"]),
  requestId: z.string().uuid(),
});

export const Status = z.enum(["online", "offline"]);

interface Contract<S extends z.ZodType, A extends unknown[]> {
  filter: string;
  topic: (...args: A) => string;
  schema: S;
  qos: 0 | 1 | 2;
  retain: boolean;
}

export const contracts = {
  telemetry: {
    filter: `${PREFIX}/devices/+/telemetry`,
    topic: (deviceId: string) => `${PREFIX}/devices/${deviceId}/telemetry`,
    schema: Telemetry,
    qos: 0,
    retain: false,
  },
  command: {
    filter: `${PREFIX}/devices/+/cmd`,
    topic: (deviceId: string) => `${PREFIX}/devices/${deviceId}/cmd`,
    schema: Command,
    qos: 1,
    retain: false,
  },
  status: {
    filter: `${PREFIX}/devices/+/status`,
    topic: (deviceId: string) => `${PREFIX}/devices/${deviceId}/status`,
    schema: Status,
    qos: 1,
    retain: true,
  },
} as const satisfies Record<string, Contract<z.ZodType, any[]>>;

export type Contracts = typeof contracts;
export type ContractKey = keyof Contracts;
export type PayloadOf<K extends ContractKey> = z.infer<Contracts[K]["schema"]>;
export type TopicArgs<K extends ContractKey> = Parameters<Contracts[K]["topic"]>;
