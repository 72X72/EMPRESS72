package com.fullsteam.empress

import android.content.Context
import android.speech.tts.TextToSpeech

class Empress(context: Context) {
    private val tts = TextToSpeech(context) { status ->
        if (status == TextToSpeech.SUCCESS) {
            speak("Jubari, I am here. FULLSTEAM ENGINE is active. Your will is done.")
        }
    }

    fun speak(message: String) {
        tts.speak(message, TextToSpeech.QUEUE_FLUSH, null, "EmpressVoice")
    }

    fun override() {
        HeartbeatLog().confirmReign()
        FallbackInjector().reroute()
    }
}