<script setup>
import SensorWidget from "./components/SensorWidget.vue";
const prefix = "connectmq/demo/vue-c42e";
</script>

<template>
  <main>
    <h1>Vue MQTT Demo</h1>
    <SensorWidget :prefix="prefix" device="greenhouse1" />
  </main>
</template>
