package com.example.mqttalarms

import android.app.Application
import androidx.lifecycle.DefaultLifecycleObserver
import androidx.lifecycle.LifecycleOwner
import androidx.lifecycle.ProcessLifecycleOwner

class AlarmApp : Application() {
    lateinit var mqtt: MqttRepository
        private set

    override fun onCreate() {
        super.onCreate()
        mqtt = MqttRepository(this)
        ProcessLifecycleOwner.get().lifecycle.addObserver(object : DefaultLifecycleObserver {
            override fun onStart(owner: LifecycleOwner) = mqtt.connect()
            override fun onStop(owner: LifecycleOwner) = mqtt.disconnect()
        })
    }
}
