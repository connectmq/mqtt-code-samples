import CocoaMQTT

let topic = "your-project/sensors/temperature" // Use a unique topic prefix: everyone can read the public broker

// Connect to the free public broker (no account needed) (Every client needs a unique client ID)
let mqtt = CocoaMQTT(clientID: "ios-" + UUID().uuidString, host: "broker.connectmq.com", port: 1883)
mqtt.keepAlive = 30

// Runs when the connection is established
mqtt.didConnectAck = { mqtt, _ in
    // Subscribe to the temperature topic
    mqtt.subscribe(topic, qos: .qos1)
    // Publish a JSON reading
    mqtt.publish(topic, withString: #"{"temperature":21.5}"#, qos: .qos1)
}
// Runs for every message on a subscribed topic
mqtt.didReceiveMessage = { _, message, _ in
    print(message.topic, message.string ?? "")
}
_ = mqtt.connect()
