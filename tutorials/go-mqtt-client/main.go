package main

import (
	"context"
	"crypto/tls"
	"encoding/json"
	"log"
	"math/rand"
	"net/url"
	"os"
	"os/signal"
	"syscall"
	"time"

	"github.com/eclipse/paho.golang/autopaho"
	"github.com/eclipse/paho.golang/paho"
)

type Reading struct {
	Device      string    `json:"device"`
	Temperature float64   `json:"temperature"`
	Timestamp   time.Time `json:"ts"`
}

func env(key, def string) string {
	if v := os.Getenv(key); v != "" {
		return v
	}
	return def
}

func main() {
	ctx, stop := signal.NotifyContext(context.Background(), os.Interrupt, syscall.SIGTERM)
	defer stop()

	serverURL, err := url.Parse(env("MQTT_URL", "tls://broker.connectmq.com:8883"))
	if err != nil {
		log.Fatal(err)
	}
	clientID := env("MQTT_CLIENT_ID", "go-demo-x9p4tz")
	prefix := env("MQTT_PREFIX", "connectmq/demo/x9p4tz")
	statusTopic := prefix + "/status"
	commandTopic := prefix + "/cmd/#"
	telemetryTopic := prefix + "/telemetry"

	cfg := autopaho.ClientConfig{
		ServerUrls:                    []*url.URL{serverURL},
		TlsCfg:                        &tls.Config{MinVersion: tls.VersionTLS12},
		KeepAlive:                     30,
		CleanStartOnInitialConnection: false,
		SessionExpiryInterval:         600,
		WillMessage: &paho.WillMessage{
			Topic:   statusTopic,
			Payload: []byte("offline"),
			QoS:     1,
			Retain:  true,
		},
		OnConnectionUp: func(cm *autopaho.ConnectionManager, connAck *paho.Connack) {
			log.Println("connected to broker")
			if _, err := cm.Subscribe(context.Background(), &paho.Subscribe{
				Subscriptions: []paho.SubscribeOptions{{Topic: commandTopic, QoS: 1}},
			}); err != nil {
				log.Printf("subscribe failed: %v", err)
			}
			if _, err := cm.Publish(context.Background(), &paho.Publish{
				Topic: statusTopic, Payload: []byte("online"), QoS: 1, Retain: true,
			}); err != nil {
				log.Printf("status publish failed: %v", err)
			}
		},
		OnConnectError: func(err error) {
			log.Printf("connection attempt failed: %v", err)
		},
		ClientConfig: paho.ClientConfig{
			ClientID: clientID,
			OnPublishReceived: []func(paho.PublishReceived) (bool, error){
				func(pr paho.PublishReceived) (bool, error) {
					log.Printf("command on %s: %s", pr.Packet.Topic, pr.Packet.Payload)
					return true, nil
				},
			},
			OnClientError: func(err error) {
				log.Printf("client error: %v", err)
			},
			OnServerDisconnect: func(d *paho.Disconnect) {
				log.Printf("server sent disconnect, reason code %d", d.ReasonCode)
			},
		},
	}

	if user := os.Getenv("MQTT_USERNAME"); user != "" {
		cfg.ConnectUsername = user
		cfg.ConnectPassword = []byte(os.Getenv("MQTT_PASSWORD"))
	}

	cm, err := autopaho.NewConnection(ctx, cfg)
	if err != nil {
		log.Fatal(err)
	}
	if err := cm.AwaitConnection(ctx); err != nil {
		log.Fatal(err)
	}

	ticker := time.NewTicker(5 * time.Second)
	defer ticker.Stop()
	expiry := uint32(60)

	for {
		select {
		case <-ticker.C:
			payload, _ := json.Marshal(Reading{
				Device:      clientID,
				Temperature: 20 + rand.Float64()*5,
				Timestamp:   time.Now().UTC(),
			})
			_, err := cm.Publish(ctx, &paho.Publish{
				Topic:   telemetryTopic,
				QoS:     1,
				Payload: payload,
				Properties: &paho.PublishProperties{
					ContentType:   "application/json",
					MessageExpiry: &expiry,
				},
			})
			if err != nil {
				log.Printf("publish failed: %v", err)
			}
		case <-ctx.Done():
			log.Println("shutting down")
			shutdownCtx, cancel := context.WithTimeout(context.Background(), 5*time.Second)
			defer cancel()
			_ = cm.Disconnect(shutdownCtx)
			<-cm.Done()
			return
		}
	}
}
