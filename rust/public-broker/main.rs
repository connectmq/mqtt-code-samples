use rumqttc::{Client, Event, MqttOptions, Packet, QoS};
use std::time::Duration;

fn main() {
    let topic = "your-project/sensors/temperature"; // Use a unique topic prefix: everyone can read the public broker

    // Connect to the free public broker (no account needed) (Every client needs a unique client ID)
    let mut options = MqttOptions::new("rust-example", "broker.connectmq.com", 1883);
    options.set_keep_alive(Duration::from_secs(30));
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
