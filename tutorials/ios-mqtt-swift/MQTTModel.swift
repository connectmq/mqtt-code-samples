import Foundation
import CocoaMQTT

@MainActor
final class MQTTModel: ObservableObject {
    @Published var isConnected = false
    @Published var readings: [String: Double] = [:]
    @Published var lastError: String?

    let topicPrefix: String
    private let mqtt: CocoaMQTT

    init(host: String = "broker.connectmq.com",
         port: UInt16 = 8883,
         username: String? = nil,
         password: String? = nil,
         clientID: String? = nil,
         topicPrefix: String? = nil) {
        let suffix = String(UUID().uuidString.prefix(8)).lowercased()
        self.topicPrefix = topicPrefix ?? "connectmq/demo/\(suffix)"
        let id = clientID ?? "ios-\(suffix)"

        mqtt = CocoaMQTT(clientID: id, host: host, port: port)
        mqtt.username = username
        mqtt.password = password
        mqtt.enableSSL = true
        mqtt.keepAlive = 30
        mqtt.cleanSession = true
        mqtt.autoReconnect = true
        mqtt.autoReconnectTimeInterval = 2
        mqtt.maxAutoReconnectTimeInterval = 60

        mqtt.didConnectAck = { [weak self] client, ack in
            Task { @MainActor in
                guard let self else { return }
                self.isConnected = (ack == .accept)
                if ack == .accept {
                    client.subscribe("\(self.topicPrefix)/sensors/+/temperature", qos: .qos1)
                } else {
                    self.lastError = "Connection rejected: \(ack)"
                }
            }
        }

        mqtt.didReceiveMessage = { [weak self] _, message, _ in
            Task { @MainActor in
                guard let self,
                      let text = message.string,
                      let value = Double(text.trimmingCharacters(in: .whitespaces)) else { return }
                // topic: <prefix>/sensors/<name>/temperature
                let parts = message.topic.split(separator: "/")
                guard parts.count >= 2 else { return }
                let name = String(parts[parts.count - 2])
                self.readings[name] = value
            }
        }

        mqtt.didDisconnect = { [weak self] _, error in
            Task { @MainActor in
                self?.isConnected = false
                if let error { self?.lastError = error.localizedDescription }
            }
        }
    }

    func connect() {
        lastError = nil
        if !mqtt.connect() {
            lastError = "Could not start connection"
        }
    }

    func disconnect() {
        mqtt.disconnect()
    }

    func setFan(_ on: Bool) {
        mqtt.publish("\(topicPrefix)/fan/set", withString: on ? "ON" : "OFF", qos: .qos1)
    }
}
