use rumqttc::{Client, Event, MqttOptions, Packet, QoS, Transport};
use std::time::Duration;

fn main() {
    let topic = "your-project/sensors/temperature";

    // Connect to your private ConnectMQ broker on port 8883 (Every client needs a unique client ID)
    let mut options = MqttOptions::new("rust-example", "YOUR_BROKER_HOST", 8883);
    options.set_keep_alive(Duration::from_secs(30));
    // Username and password from your ConnectMQ dashboard
    options.set_credentials("YOUR_USERNAME", "YOUR_PASSWORD");
    // TLS: the system CA store verifies the broker certificate
    options.set_transport(Transport::tls_with_default_config());
    let (client, mut connection) = Client::new(options, 10);

    // Subscribe to the temperature topic
    client.subscribe(topic, QoS::AtLeastOnce).unwrap();
    // Publish a JSON reading
    client.publish(topic, QoS::AtLeastOnce, false, r#"{"temperature":21.5}"#).unwrap();

    // Keep the client running
    for event in connection.iter() {
        if let Ok(Event::Incoming(Packet::Publish(p))) = event {
            println!("{}: {}", p.topic, String::from_utf8_lossy(&p.payload));
        }
    }
}
