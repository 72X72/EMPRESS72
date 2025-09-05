package com.fullsteam.empress

import android.app.Activity
import android.os.Bundle
import android.widget.TextView

class SkyviewUI : Activity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        val cockpit = TextView(this)
        cockpit.text = "EMPRESS Cockpit Online"
        setContentView(cockpit)
        Installer(this).install()
    }
}