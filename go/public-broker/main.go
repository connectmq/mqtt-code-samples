package main

import (
	"fmt"
	"time"

	mqtt "github.com/eclipse/paho.mqtt.golang"
)

func main() {
	topic := "your-project/sensors/temperature" // Use a unique topic prefix: everyone can read the public broker

	// Connect to the free public broker (no account needed)
	opts := mqtt.NewClientOptions().AddBroker("tcp://broker.connectmq.com:1883")
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
