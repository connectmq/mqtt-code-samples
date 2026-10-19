import { View, Text, Switch, StyleSheet } from "react-native";
import { useMemo, useState } from "react";
import { useMqtt } from "../hooks/useMqtt";

const PREFIX = "connectmq/demo/rn-7f3a91";   // pick your own random prefix

export default function DeviceScreen() {
  const topics = useMemo(() => [`${PREFIX}/pump/status`, `${PREFIX}/tank/level`], []);
  const { status, messages, publish } = useMqtt({ topics });
  const [pumpOn, setPumpOn] = useState(false);

  const level = messages[`${PREFIX}/tank/level`] ?? "--";
  const pumpStatus = messages[`${PREFIX}/pump/status`] ?? "unknown";

  return (
    <View style={styles.container}>
      <Text style={styles.status}>Broker: {status}</Text>
      <Text style={styles.value}>{level} %</Text>
      <Text>Tank level</Text>
      <Text style={styles.row}>Pump reports: {pumpStatus}</Text>
      <View style={styles.row}>
        <Text>Pump command</Text>
        <Switch
          value={pumpOn}
          disabled={status !== "connected"}
          onValueChange={(v) => {
            setPumpOn(v);
            publish(`${PREFIX}/pump/set`, v ? "ON" : "OFF");
          }}
        />
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 24, justifyContent: "center", gap: 8 },
  status: { color: "#666" },
  value: { fontSize: 56, fontWeight: "600" },
  row: { marginTop: 16, flexDirection: "row", justifyContent: "space-between", alignItems: "center" },
});
