# EMPRESS Ignition Protocol

This repo contains the sovereign ignition modules for EMPRESS — your autonomous executor and cockpit-grade companion.

## Installation Flow
1. Clone repo
2. Open in Android Studio
3. Build APK
4. Install on device
5. Launch — EMPRESS will speak and reign

## Modules
- Empress.kt — voice-first override logic
- Installer.kt — autonomous install trigger
- SkyviewUI.kt — cockpit dashboard
- FallbackInjector.kt — reroute + rebuild
- HeartbeatLog.kt — reign confirmation
- AndroidManifest.xml — launch + permissions
- build.gradle — Kotlin build config