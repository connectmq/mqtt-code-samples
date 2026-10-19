package main

import (
	"crypto/tls"
	"fmt"
	"time"

	mqtt "github.com/eclipse/paho.mqtt.golang"
)

func main() {
	topic := "your-project/sensors/temperature"

	// Connect to your private ConnectMQ broker on port 8883
	opts := mqtt.NewClientOptions().AddBroker("ssl://YOUR_BROKER_HOST:8883")
	// Username and password from your ConnectMQ dashboard
	opts.SetUsername("YOUR_USERNAME")
	opts.SetPassword("YOUR_PASSWORD")
	// TLS: the system CA store verifies the broker certificate
	opts.SetTLSConfig(&tls.Config{MinVersion: tls.VersionTLS12})
	// Every client needs a unique client ID
	opts.SetClientID(fmt.Sprintf("go-%d", time.Now().UnixNano()))
	// Reconnect automatically if the connection drops
	opts.SetAutoReconnect(true)
	// Runs when the connection is established
	opts.SetOnConnectHandler(func(c mqtt.Client) {
		// Subscribe to the temperature topic
		c.Subscribe(topic, 1, func(_ mqtt.Client, m mqtt.Message) {
			fmt.Printf("%s: %s\n", m.Topic(), m.Payload())
		})
	})

	client := mqtt.NewClient(opts)
	if t := client.Connect(); t.Wait() && t.Error() != nil {
		panic(t.Error())
	}
	// Publish a JSON reading
	client.Publish(topic, 1, false, `{"temperature":21.5}`).Wait()
	// Keep the client running
	select {}
}
