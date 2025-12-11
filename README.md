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

![ezgif-82c28b73b4d19322](https://github.com/user-attachments/assets/732899fc-de32-4af3-9548-dfbcbad1e728)















_____________________________________________________________________________________________________________________________

# Nexus Monitor (Archived Experimental Project)

Nexus Monitor is a personal experiment that turns a Windows PC into a local stats server and shows live CPU/GPU/RAM data on an Android phone UI.

⚠️ **Status: Archived / Experimental**

This project was built in a few intense days by a student as a learning project.  
It works reliably on the original developer’s PC, but **it is not a polished, plug‑and‑play app for all systems.**

### What this project does

- Runs a Python + LibreHardwareMonitor server on Windows to read hardware stats. [memory:1]
- Shows those stats on a custom Android app UI (originally called Perpu Monitor, later Nexus Monitor). [memory:11]
- Includes some scripts to help install Python dependencies and start the server. [memory:78]

### Known limitations

- Requires a specific Windows setup (Python, Visual C++ runtime, .NET / LHM, firewall rules).
- Some users report:
  - `vcruntime140.dll` or other missing runtime errors. [web:108][web:111]
  - Server not starting or closing immediately.
  - Network issues when phone and PC are not on the same LAN.
- This project was never fully tested across many different PCs / GPUs / Windows versions.

### Why it’s archived

This started as a **personal tool** and a way to learn about:
- Python, Flask, and local APIs.
- Reading hardware sensors via LibreHardwareMonitor.
- Connecting a phone UI to a PC over the local network. [memory:1][memory:12]

During testing on other machines, it became clear that:
- Packaging Python apps and native DLLs for “any Windows PC” is much harder than expected.
- Fixing all edge cases would require more time, experience, and testing than a solo student can give right now. [web:107]

So the project is now **archived as-is**:
- **No further fixes or support are planned.**
- The code is left here as a reference for anyone who wants to learn from it or fork it.

### If you want to use this

- Treat it as sample code / a learning reference.
- Expect to debug Python, paths, and runtimes on your own machine.
- Do **not** expect a one-click installer that works everywhere.

### What I learned

- “It works on my PC” is very different from “it works on everyone’s PC.”
- Packaging, installers, and runtimes are as important as the core idea. [web:107]
- Real monitoring tools need lots of defensive coding and testing.
- Building and shipping something, even imperfect, teaches more than 100 tutorials.

Thanks to everyone who tried it, sent feedback, or even just starred the repo.

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

