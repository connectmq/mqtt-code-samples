import CocoaMQTT

let topic = "your-project/sensors/temperature"

// Connect to your private ConnectMQ broker on port 8883 (Every client needs a unique client ID)
let mqtt = CocoaMQTT(clientID: "ios-" + UUID().uuidString, host: "YOUR_BROKER_HOST", port: 8883)
mqtt.keepAlive = 30
// Username and password from your ConnectMQ dashboard
mqtt.username = "YOUR_USERNAME"
mqtt.password = "YOUR_PASSWORD"
// TLS: the system CA store verifies the broker certificate
mqtt.enableSSL = true

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
