# app/services/device_commands.rb
require Rails.root.join("lib/tls_client")

class DeviceCommands
  def self.send!(device_id, action)
    raise ArgumentError, "bad device" unless device_id.to_s.match?(/\A[a-z0-9_-]+\z/i)

    topic = "#{ENV.fetch('MQTT_TOPIC_PREFIX')}/devices/#{device_id}/set"
    client = build_client(client_id: "#{ENV.fetch('MQTT_CLIENT_ID_PREFIX', 'rails')}-pub-#{SecureRandom.hex(3)}")
    client.connect
    client.publish(topic, { action: action, ts: Time.now.to_i }.to_json, false, 1)
  ensure
    client&.disconnect
  end
end
