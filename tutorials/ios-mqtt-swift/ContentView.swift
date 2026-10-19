import SwiftUI

struct ContentView: View {
    @StateObject private var model = MQTTModel()
    @State private var fanOn = false
    @Environment(\.scenePhase) private var scenePhase

    var body: some View {
        NavigationStack {
            List {
                Section("Connection") {
                    Label(model.isConnected ? "Connected" : "Disconnected",
                          systemImage: model.isConnected ? "checkmark.circle" : "xmark.circle")
                    if let err = model.lastError {
                        Text(err).foregroundStyle(.red).font(.footnote)
                    }
                    Text(model.topicPrefix).font(.caption).textSelection(.enabled)
                }
                Section("Sensors") {
                    if model.readings.isEmpty {
                        Text("Waiting for data...").foregroundStyle(.secondary)
                    }
                    ForEach(model.readings.keys.sorted(), id: \.self) { name in
                        HStack {
                            Text(name.capitalized)
                            Spacer()
                            Text(String(format: "%.1f °C", model.readings[name] ?? 0))
                                .monospacedDigit()
                        }
                    }
                }
                Section("Commands") {
                    Toggle("Fan", isOn: $fanOn)
                        .onChange(of: fanOn) { _, newValue in model.setFan(newValue) }
                        .disabled(!model.isConnected)
                }
            }
            .navigationTitle("iOS MQTT Demo")
        }
        .onAppear { model.connect() }
        .onChange(of: scenePhase) { _, phase in
            switch phase {
            case .active: model.connect()
            case .background: model.disconnect()
            default: break
            }
        }
    }
}
