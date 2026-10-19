require "json"
require_relative "tls_client"

class MqttWorker
  RETRYABLE = [MQTT::Exception, SocketError, IOError, SystemCallError,
               OpenSSL::SSL::SSLError, Timeout::Error].freeze

  def initialize(filter:, handler:)
    @filter = filter
    @handler = handler
    @running = true
  end

  def stop
    @running = false
    @client&.disconnect rescue nil
  end

  def run
    backoff = 1
    while @running
      begin
        @client = build_client
        @client.connect
        @client.subscribe(@filter => 1)
        warn "connected, subscribed to #{@filter}"
        backoff = 1

        @client.get do |topic, payload|
          handle(topic, payload)
          break unless @running
        end
      rescue *RETRYABLE => e
        break unless @running
        warn "mqtt error: #{e.class}: #{e.message}; retrying in #{backoff}s"
        sleep backoff
        backoff = [backoff * 2, 60].min
      ensure
        @client&.disconnect rescue nil
      end
    end
  end

  private

  def handle(topic, payload)
    data = JSON.parse(payload)
    @handler.call(topic, data)
  rescue JSON::ParserError
    warn "ignoring non-JSON payload on #{topic}"
  rescue StandardError => e
    warn "handler failed for #{topic}: #{e.class}: #{e.message}"
  end
end

if $PROGRAM_NAME == __FILE__
  prefix = ENV.fetch("MQTT_TOPIC_PREFIX", "connectmq/demo/ruby-worker-7c2e")
  worker = MqttWorker.new(
    filter: "#{prefix}/devices/+/telemetry",
    handler: ->(topic, data) { puts "#{topic.split('/')[-2]}: #{data.inspect}" }
  )
  %w[INT TERM].each { |sig| trap(sig) { Thread.new { worker.stop } } }
  worker.run
end
