use rumqttc::{AsyncClient, Event, MqttOptions, Packet, QoS};
use std::time::Duration;

#[tokio::main]
async fn main() {
    let topic = "connectmq/demo/k3x8p1/libs/rust";
    let mut opts = MqttOptions::new("libs-rust-k3x8p1", "broker.connectmq.com", 1883);
    opts.set_keep_alive(Duration::from_secs(30));

    let (client, mut eventloop) = AsyncClient::new(opts, 10);
    client.subscribe(topic, QoS::AtLeastOnce).await.unwrap();
    client.publish(topic, QoS::AtLeastOnce, false, "hello from rumqttc").await.unwrap();

    loop {
        match eventloop.poll().await {
            Ok(Event::Incoming(Packet::Publish(p))) => {
                println!("{} {}", p.topic, String::from_utf8_lossy(&p.payload));
            }
            Ok(_) => {}
            Err(e) => {
                eprintln!("connection error: {e}");
                tokio::time::sleep(Duration::from_secs(2)).await;
            }
        }
    }
}
