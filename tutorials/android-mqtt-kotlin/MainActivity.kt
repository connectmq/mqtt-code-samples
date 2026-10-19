package com.example.mqttalarms

import android.Manifest
import android.os.Build
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.collectAsState
import androidx.compose.runtime.getValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp

class MainActivity : ComponentActivity() {
    private val requestPermission =
        registerForActivityResult(ActivityResultContracts.RequestPermission()) { }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        if (Build.VERSION.SDK_INT >= 33) {
            requestPermission.launch(Manifest.permission.POST_NOTIFICATIONS)
        }
        val mqtt = (application as AlarmApp).mqtt
        setContent {
            MaterialTheme {
                val connected by mqtt.connected.collectAsState()
                val alarm by mqtt.lastAlarm.collectAsState()
                Column(Modifier.padding(24.dp)) {
                    Text(if (connected) "Connected to broker" else "Disconnected")
                    Text("Last alarm: $alarm", style = MaterialTheme.typography.titleMedium)
                }
            }
        }
    }
}
