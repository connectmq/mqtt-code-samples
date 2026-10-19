<script setup>
import { computed } from "vue";
import { useMqtt } from "../composables/useMqtt";

const props = defineProps({
  prefix: { type: String, required: true },
  device: { type: String, required: true },
});

const clientId = `vue-${Math.random().toString(16).slice(2, 10)}`;
const telemetryTopic = `${props.prefix}/${props.device}/telemetry`;

const { status, messages, publish } = useMqtt(
  "wss://broker.connectmq.com:8084/mqtt",
  { clientId },
  [telemetryTopic]
);

const reading = computed(() => messages[telemetryTopic]?.value ?? {});
const updatedAt = computed(() => {
  const ts = messages[telemetryTopic]?.receivedAt;
  return ts ? new Date(ts).toLocaleTimeString() : "never";
});

function toggleFan() {
  publish(`${props.prefix}/${props.device}/cmd`, { action: "toggle-fan" }, { qos: 1 });
}
</script>

<template>
  <div class="widget">
    <header>
      <h3>{{ device }}</h3>
      <span :class="['status', status]">{{ status }}</span>
    </header>
    <p class="big">{{ reading.temperature ?? "--" }} &deg;C</p>
    <p>Humidity: {{ reading.humidity ?? "--" }} %</p>
    <small>Updated: {{ updatedAt }}</small>
    <button :disabled="status !== 'connected'" @click="toggleFan">Toggle fan</button>
  </div>
</template>

<style scoped>
.widget { border: 1px solid #ccc; border-radius: 8px; padding: 1rem; max-width: 280px; }
.big { font-size: 2rem; margin: 0.5rem 0; }
.status.connected { color: green; }
.status.reconnecting, .status.offline { color: orange; }
</style>
