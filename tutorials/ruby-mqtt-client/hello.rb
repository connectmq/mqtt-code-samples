require "mqtt"
require "securerandom"

PREFIX = "connectmq/demo/ruby-#{SecureRandom.hex(4)}"

subscriber = Thread.new do
  MQTT::Client.connect(host: "broker.connectmq.com", port: 1883,
                       client_id: "ruby-sub-#{SecureRandom.hex(4)}") do |c|
    c.get("#{PREFIX}/#") do |topic, message|
      puts "received #{topic}: #{message}"
      break if message == "bye"
    end
  end
end

sleep 1 # give the subscriber time to subscribe

MQTT::Client.connect(host: "broker.connectmq.com", port: 1883,
                     client_id: "ruby-pub-#{SecureRandom.hex(4)}") do |c|
  c.publish("#{PREFIX}/greeting", "hello from Ruby")
  c.publish("#{PREFIX}/greeting", "bye")
end

subscriber.join
