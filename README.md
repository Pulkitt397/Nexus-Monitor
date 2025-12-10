# Nexus Monitor v1.0

Nexus Monitor is a real-time PC dashboard and AI assistant that turns your Android phone into a secondary status display.

## 1. Android App Setup
- Transfer `apk/Nexus-v1.0.apk` to your phone.
- Install the APK.
- Connect your phone to the same WiFi as your PC.

## 2. PC Server Setup (One-Click)
1. Open the `server` folder on your PC.
2. **First Time Only:** Double-click     install_dependencies.bat to automatically install required Python libraries.
3. **Start Server:** Double-click `start.vbs`.
   - This runs silently in the background.
   - *Note: Press YES if asked for Administrator permission (Required for Hardware Monitor & Gaming Mode).*

*(Optional: Use `startwithlogs.bat` if you need to see debug errors window).*

## 3. How to Stop
- Double-click `stop_server.bat` to cleanly close the Server and Hardware Monitor.

## 4. Troubleshooting
- **Firewall:** If the app stays on "0", open Windows Firewall settings and allow `python.exe` through both Private and Public networks.
- **Network:** Ensure your Phone and PC are connected to the exact same WiFi router/band.
