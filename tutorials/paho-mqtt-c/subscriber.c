#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <signal.h>
#include <time.h>
#include <unistd.h>
#include "MQTTClient.h"

#define ADDRESS   "ssl://broker.connectmq.com:8883"
#define CA_BUNDLE "/etc/ssl/certs/ca-certificates.crt"
#define QOS       1
#define TIMEOUT   10000L

static volatile sig_atomic_t running = 1;
static void on_signal(int sig) { (void)sig; running = 0; }

static void connection_lost(void *ctx, char *cause) {
    (void)ctx;
    fprintf(stderr, "connection lost: %s\n", cause ? cause : "unknown");
}

static int message_arrived(void *ctx, char *topic, int len, MQTTClient_message *msg) {
    (void)ctx; (void)len;
    MQTTClient_freeMessage(&msg);
    MQTTClient_free(topic);
    return 1;
}

static int connect_broker(MQTTClient client) {
    MQTTClient_connectOptions opts = MQTTClient_connectOptions_initializer;
    MQTTClient_SSLOptions ssl = MQTTClient_SSLOptions_initializer;

    ssl.trustStore = CA_BUNDLE;
    ssl.enableServerCertAuth = 1;
    ssl.verify = 1;                       /* check the hostname too */
    ssl.sslVersion = MQTT_SSL_VERSION_TLS_1_2;

    opts.keepAliveInterval = 30;
    opts.cleansession = 1;
    opts.ssl = &ssl;
    opts.username = getenv("MQTT_USERNAME");   /* NULL = anonymous */
    opts.password = getenv("MQTT_PASSWORD");

    int rc = MQTTClient_connect(client, &opts);
    if (rc != MQTTCLIENT_SUCCESS)
        fprintf(stderr, "connect failed, rc=%d\n", rc);
    return rc;
}

static int on_message(void *ctx, char *topic, int len, MQTTClient_message *msg) {
    (void)ctx; (void)len;
    printf("%s: %.*s\n", topic, msg->payloadlen, (char *)msg->payload);
    MQTTClient_freeMessage(&msg);
    MQTTClient_free(topic);
    return 1;   /* 1 = message handled; 0 asks the library to redeliver */
}

int main(void) {
    const char *prefix = getenv("MQTT_TOPIC_PREFIX");
    char filter[256];
    if (!prefix) prefix = "connectmq/demo/paho-c-4821";
    snprintf(filter, sizeof filter, "%s/+/temperature", prefix);

    signal(SIGINT, on_signal);
    signal(SIGTERM, on_signal);

    MQTTClient client;
    MQTTClient_create(&client, ADDRESS, "paho-c-sub-4821",
                      MQTTCLIENT_PERSISTENCE_NONE, NULL);
    MQTTClient_setCallbacks(client, NULL, connection_lost, on_message, NULL);

    while (running) {
        if (!MQTTClient_isConnected(client)) {
            if (connect_broker(client) == MQTTCLIENT_SUCCESS) {
                MQTTClient_subscribe(client, filter, QOS);
                printf("subscribed to %s\n", filter);
            } else {
                sleep(5);
                continue;
            }
        }
        sleep(1);
    }
    MQTTClient_disconnect(client, TIMEOUT);
    MQTTClient_destroy(&client);
    return 0;
}
