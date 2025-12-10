# Nexus Monitor v3.0

Nexus Monitor is a real-time PC dashboard and AI assistant that turns your Android phone into a secondary status display.

## What's new (v3.0.0)

- Added two-way clipboard sync between PC and Android.
- Added file sharing from phone to a dedicated folder on Windows.
- New elevated launcher that starts LibreHardwareMonitor minimized and runs the Nexus server in the background.
_____________________________________________________________________________________________________________________________

![Screenshot_20251210_194413](https://github.com/user-attachments/assets/bc034bda-5f7f-41b5-b913-4be18bde2e1d)

![Screenshot_20251210_194427](https://github.com/user-attachments/assets/931492fb-223a-4390-a6b7-ce0389d84f70)

![Screenshot_20251210_194422](https://github.com/user-attachments/assets/81fbd18d-dbba-407d-9cb4-9423f42d2421)

![Screenshot_20251210_194444](https://github.com/user-attachments/assets/5e2edea0-f197-486c-984d-60b6c041f92e)

![Screenshot_20251210_194452](https://github.com/user-attachments/assets/c112e1f0-54e5-4dc4-835f-622c4f8804c9)

![Screenshot_20251210_194459](https://github.com/user-attachments/assets/2ab71faa-a4e0-4089-a5bf-401d70efb28d)

https://github.com/user-attachments/assets/f0ec8b10-9438-47be-84f0-52be2be1517c















_____________________________________________________________________________________________________________________________
## 1. Android App Setup

- Transfer `apk/Nexus-Monitor-v3.0.apk` to your phone.
- Install the APK.
- Connect your phone to the same WiFi as your PC.

## 2. PC Server Setup (One-Click)

1. Open the `server` folder on your PC.
2. **First Time Only:** Double-click `install_dependencies.bat` to automatically install required Python libraries.
3. **Start Server:** Double-click `start.vbs`.
   - This runs silently in the background.
   - *Note: Press YES if asked for Administrator permission (required for Hardware Monitor, clipboard sync, file sharing, and Gaming Mode).*
4. Ensure `LibreHardwareMonitor` folder is present inside `server` (it is started automatically by the scripts).

*(Optional: Use `startwithlogs.bat` if you need to see a debug/log window instead of running fully silent.)*

## 3. How to Stop

- Double-click `stop_server.bat` to cleanly close the Nexus Server and LibreHardwareMonitor.

## 4. Troubleshooting

- **Firewall:** If the app stays on "0" or cannot connect, open Windows Firewall settings and allow `Nexus-Server.exe` (or `python.exe` if running from source) through both Private and Public networks.
- **Network:** Ensure your phone and PC are connected to the exact same WiFi router/band (e.g., both on 2.4 GHz or both on 5 GHz).
- **Admin prompt missing:** If hardware stats or clipboard/file features don’t work, make sure you started the server via `start.vbs` and accepted the Administrator UAC prompt.

## 5. Changelog

- v3.0.0
  - Added clipboard sync and file sharing.
  - New admin launcher (`start.vbs` + `start_silent.bat`) that auto-starts LibreHardwareMonitor and the server.
  - Improved hardware stats smoothing and updated helper scripts.

