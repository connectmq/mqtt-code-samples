use rumqttc::{AsyncClient, Event, LastWill, MqttOptions, Packet, QoS, Transport};
use serde::Serialize;
use std::env;
use std::time::{Duration, SystemTime, UNIX_EPOCH};
use tokio::time;

#[derive(Serialize)]
struct Reading {
    device: String,
    temperature: f64,
    ts: u64,
}

fn var(key: &str, default: &str) -> String {
    env::var(key).unwrap_or_else(|_| default.to_string())
}

#[tokio::main]
async fn main() {
    let host = var("MQTT_HOST", "broker.connectmq.com");
    let client_id = var("MQTT_CLIENT_ID", "rust-demo-m3c8wd");
    let prefix = var("MQTT_PREFIX", "connectmq/demo/m3c8wd");
    let status_topic = format!("{prefix}/status");
    let command_filter = format!("{prefix}/cmd/#");
    let telemetry_topic = format!("{prefix}/telemetry");

    let mut options = MqttOptions::new(client_id.clone(), host, 8883);
    options.set_keep_alive(Duration::from_secs(30));
    options.set_clean_session(false);
    options.set_last_will(LastWill::new(&status_topic, "offline", QoS::AtLeastOnce, true));
    options.set_transport(Transport::tls_with_default_config());
    if let Ok(user) = env::var("MQTT_USERNAME") {
        options.set_credentials(user, env::var("MQTT_PASSWORD").unwrap_or_default());
    }

    let (client, mut eventloop) = AsyncClient::new(options, 32);

    // Publisher task: sends a reading every 5 seconds.
    let publisher = client.clone();
    let device = client_id.clone();
    tokio::spawn(async move {
        let mut ticker = time::interval(Duration::from_secs(5));
        let mut temperature = 21.0_f64;
        loop {
            ticker.tick().await;
            temperature += 0.1;
            let ts = SystemTime::now().duration_since(UNIX_EPOCH).unwrap().as_secs();
            let reading = Reading { device: device.clone(), temperature, ts };
            let payload = serde_json::to_vec(&reading).expect("serialize");
            if let Err(e) = publisher
                .publish(&telemetry_topic, QoS::AtLeastOnce, false, payload)
                .await
            {
                eprintln!("publish request failed: {e}");
            }
        }
    });

    // Event loop: drives the connection, handles reconnects and incoming messages.
    loop {
        match eventloop.poll().await {
            Ok(Event::Incoming(Packet::ConnAck(ack))) => {
                println!("connected: {:?}", ack.code);
                // Non-blocking requests: never await the client inside the poll loop.
                if let Err(e) = client.try_subscribe(&command_filter, QoS::AtLeastOnce) {
                    eprintln!("subscribe request failed: {e}");
                }
                if let Err(e) = client.try_publish(&status_topic, QoS::AtLeastOnce, true, "online") {
                    eprintln!("status request failed: {e}");
                }
            }
            Ok(Event::Incoming(Packet::Publish(msg))) => {
                println!("command on {}: {}", msg.topic, String::from_utf8_lossy(&msg.payload));
            }
            Ok(_) => {}
            Err(e) => {
                eprintln!("connection error: {e}; reconnecting in 5 s");
                time::sleep(Duration::from_secs(5)).await;
            }
        }
    }
}
