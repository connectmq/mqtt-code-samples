#include <stdio.h>
#include <string.h>
#include "MQTTClient.h"

int main(void) {
    MQTTClient client;
    MQTTClient_connectOptions opts = MQTTClient_connectOptions_initializer;
    MQTTClient_message msg = MQTTClient_message_initializer;
    MQTTClient_deliveryToken token;
    const char *topic = "connectmq/demo/k3x8p1/libs/c";
    char payload[] = "hello from Paho C";

    MQTTClient_create(&client, "tcp://broker.connectmq.com:1883", "libs-c-k3x8p1",
                      MQTTCLIENT_PERSISTENCE_NONE, NULL);
    opts.keepAliveInterval = 30;
    opts.cleansession = 1;

    if (MQTTClient_connect(client, &opts) != MQTTCLIENT_SUCCESS) {
        fprintf(stderr, "connect failed\n");
        return 1;
    }

    msg.payload = payload;
    msg.payloadlen = (int)strlen(payload);
    msg.qos = 1;
    msg.retained = 0;
    MQTTClient_publishMessage(client, topic, &msg, &token);
    MQTTClient_waitForCompletion(client, token, 10000L);

    MQTTClient_disconnect(client, 10000);
    MQTTClient_destroy(&client);
    return 0;
}
