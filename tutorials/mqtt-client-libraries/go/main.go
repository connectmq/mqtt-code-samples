package main

import (
	"crypto/tls"
	"fmt"
	"math/rand"
	"time"

	mqtt "github.com/eclipse/paho.mqtt.golang"
)

func main() {
	topic := "connectmq/demo/k3x8p1/libs/go"
	opts := mqtt.NewClientOptions().
		AddBroker("tls://broker.connectmq.com:8883").
		SetClientID(fmt.Sprintf("libs-go-%06d", rand.Intn(1000000))).
		SetTLSConfig(&tls.Config{MinVersion: tls.VersionTLS12}).
		SetAutoReconnect(true)

	client := mqtt.NewClient(opts)
	if token := client.Connect(); token.Wait() && token.Error() != nil {
		panic(token.Error())
	}

	client.Subscribe(topic, 1, func(_ mqtt.Client, m mqtt.Message) {
		fmt.Printf("%s %s\n", m.Topic(), m.Payload())
	}).Wait()

	client.Publish(topic, 1, false, "hello from Go").Wait()
	time.Sleep(2 * time.Second)
	client.Disconnect(250)
}
