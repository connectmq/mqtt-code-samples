import { createContext, useContext, useState } from "react";
import { useMqtt } from "./useMqtt";

const MqttContext = createContext(null);

export function MqttProvider({ url, topics, children }) {
  const [clientId] = useState(() => `react-${Math.random().toString(16).slice(2, 10)}`);
  const mqttState = useMqtt(url, { clientId }, topics);
  return <MqttContext.Provider value={mqttState}>{children}</MqttContext.Provider>;
}

export function useMqttContext() {
  const value = useContext(MqttContext);
  if (!value) throw new Error("useMqttContext must be used inside MqttProvider");
  return value;
}
