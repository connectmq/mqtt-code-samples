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

int main(void) {
    const char *client_id = getenv("MQTT_CLIENT_ID");
    const char *prefix = getenv("MQTT_TOPIC_PREFIX");
    char id_buf[64], topic[256], payload[128];

    if (!client_id) {
        snprintf(id_buf, sizeof id_buf, "paho-c-%d", (int)getpid());
        client_id = id_buf;
    }
    if (!prefix) prefix = "connectmq/demo/paho-c-4821";
    snprintf(topic, sizeof topic, "%s/gateway1/temperature", prefix);

    signal(SIGINT, on_signal);
    signal(SIGTERM, on_signal);

    MQTTClient client;
    int rc = MQTTClient_create(&client, ADDRESS, client_id,
                               MQTTCLIENT_PERSISTENCE_NONE, NULL);
    if (rc != MQTTCLIENT_SUCCESS) {
        fprintf(stderr, "create failed, rc=%d\n", rc);
        return EXIT_FAILURE;
    }
    MQTTClient_setCallbacks(client, NULL, connection_lost, message_arrived, NULL);

    int backoff = 1;
    while (running && connect_broker(client) != MQTTCLIENT_SUCCESS) {
        sleep(backoff);
        if (backoff < 60) backoff *= 2;
    }
    printf("connected as %s, publishing to %s\n", client_id, topic);

    srand((unsigned)time(NULL));
    while (running) {
        if (!MQTTClient_isConnected(client)) {
            if (connect_broker(client) != MQTTCLIENT_SUCCESS) { sleep(5); continue; }
        }

        double temp = 20.0 + (rand() % 100) / 10.0;
        int n = snprintf(payload, sizeof payload,
                         "{\"ts\":%ld,\"temperature\":%.1f}", (long)time(NULL), temp);

        MQTTClient_message msg = MQTTClient_message_initializer;
        MQTTClient_deliveryToken token;
        msg.payload = payload;
        msg.payloadlen = n;
        msg.qos = QOS;
        msg.retained = 0;

        rc = MQTTClient_publishMessage(client, topic, &msg, &token);
        if (rc == MQTTCLIENT_SUCCESS)
            rc = MQTTClient_waitForCompletion(client, token, TIMEOUT);
        if (rc != MQTTCLIENT_SUCCESS)
            fprintf(stderr, "publish failed, rc=%d\n", rc);
        else
            printf("sent %s\n", payload);

        sleep(5);
    }

    MQTTClient_disconnect(client, TIMEOUT);
    MQTTClient_destroy(&client);
    return EXIT_SUCCESS;
}
