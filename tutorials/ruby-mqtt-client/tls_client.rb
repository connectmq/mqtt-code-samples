require "mqtt"
require "openssl"
require "securerandom"

def build_client(client_id: nil)
  client = MQTT::Client.new
  client.host = ENV.fetch("MQTT_HOST", "broker.connectmq.com")
  client.port = 8883
  client.ssl = true
  client.ssl_context.set_params(verify_mode: OpenSSL::SSL::VERIFY_PEER)
  client.username = ENV["MQTT_USERNAME"]          # nil = anonymous (public broker)
  client.password = ENV["MQTT_PASSWORD"]
  client.client_id = client_id || ENV["MQTT_CLIENT_ID"] || "ruby-#{SecureRandom.hex(4)}"
  client.keep_alive = 30
  client.clean_session = true
  client
end

if $PROGRAM_NAME == __FILE__
  client = build_client
  client.connect
  client.publish("connectmq/demo/ruby-tls-test/status", "online", false, 1)
  puts "published over TLS as #{client.client_id}"
  client.disconnect
end
