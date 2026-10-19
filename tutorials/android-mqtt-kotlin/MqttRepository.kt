package com.example.mqttalarms

import android.app.NotificationChannel
import android.app.NotificationManager
import android.content.Context
import android.util.Log
import androidx.core.app.NotificationCompat
import androidx.core.app.NotificationManagerCompat
import com.hivemq.client.mqtt.MqttClient
import com.hivemq.client.mqtt.datatypes.MqttQos
import com.hivemq.client.mqtt.mqtt5.Mqtt5AsyncClient
import com.hivemq.client.mqtt.mqtt5.message.publish.Mqtt5Publish
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import java.util.UUID
import java.util.concurrent.TimeUnit
import java.util.concurrent.atomic.AtomicInteger

class MqttRepository(private val context: Context) {

    companion object {
        const val PREFIX = "connectmq/demo/a7k2"
        private const val CHANNEL_ID = "alarms"
        private const val TAG = "MqttRepository"
    }

    private val _connected = MutableStateFlow(false)
    val connected: StateFlow<Boolean> = _connected

    private val _lastAlarm = MutableStateFlow("No alarms yet")
    val lastAlarm: StateFlow<String> = _lastAlarm

    private val notificationId = AtomicInteger(1000)

    private val clientId: String by lazy {
        val prefs = context.getSharedPreferences("mqtt", Context.MODE_PRIVATE)
        prefs.getString("client_id", null) ?: ("android-" + UUID.randomUUID().toString().take(12))
            .also { prefs.edit().putString("client_id", it).apply() }
    }

    private val client: Mqtt5AsyncClient by lazy {
        MqttClient.builder()
            .useMqttVersion5()
            .identifier(clientId)
            .serverHost("broker.connectmq.com")
            .serverPort(8883)
            .sslWithDefaultConfig()
            .automaticReconnect()
                .initialDelay(1, TimeUnit.SECONDS)
                .maxDelay(30, TimeUnit.SECONDS)
                .applyAutomaticReconnect()
            .addConnectedListener { _connected.value = true; Log.i(TAG, "connected") }
            .addDisconnectedListener { ctx ->
                _connected.value = false
                Log.w(TAG, "disconnected: ${ctx.cause.message} (source ${ctx.source})")
            }
            .buildAsync()
    }

    init {
        val channel = NotificationChannel(CHANNEL_ID, "Device alarms",
            NotificationManager.IMPORTANCE_HIGH)
        context.getSystemService(NotificationManager::class.java)
            .createNotificationChannel(channel)
    }

    fun connect() {
        if (client.state.isConnectedOrReconnect) return
        client.connectWith()
            .cleanStart(true)
            .keepAlive(30)
            .send()
            .whenComplete { connAck, error ->
                if (error != null) {
                    Log.e(TAG, "connect failed", error)
                } else {
                    Log.i(TAG, "CONNACK ${connAck.reasonCode}")
                    subscribe()
                }
            }
    }

    private fun subscribe() {
        client.subscribeWith()
            .topicFilter("$PREFIX/+/alarm")
            .qos(MqttQos.AT_LEAST_ONCE)
            .callback(::onAlarm)
            .send()
            .whenComplete { subAck, error ->
                if (error != null) Log.e(TAG, "subscribe failed", error)
                else Log.i(TAG, "SUBACK ${subAck.reasonCodes}")
            }
    }

    private fun onAlarm(publish: Mqtt5Publish) {
        // Runs on the client's network thread: no UI work here, only thread-safe calls
        val device = publish.topic.levels.getOrNull(3) ?: "unknown"
        val text = String(publish.payloadAsBytes, Charsets.UTF_8)
        _lastAlarm.value = "$device: $text"
        showNotification(device, text)
    }

    private fun showNotification(device: String, text: String) {
        val nm = NotificationManagerCompat.from(context)
        if (!nm.areNotificationsEnabled()) return
        val notification = NotificationCompat.Builder(context, CHANNEL_ID)
            .setSmallIcon(android.R.drawable.stat_sys_warning)
            .setContentTitle("Alarm on $device")
            .setContentText(text)
            .setPriority(NotificationCompat.PRIORITY_HIGH)
            .setAutoCancel(true)
            .build()
        try {
            nm.notify(notificationId.incrementAndGet(), notification)
        } catch (e: SecurityException) {
            Log.w(TAG, "notification permission missing")
        }
    }

    fun disconnect() {
        if (client.state.isConnected) client.disconnect()
    }
}
