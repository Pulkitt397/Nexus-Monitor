@echo off
cd /d "%~dp0"

:: 1. Start LibreHardwareMonitor (Minimized)
cd LibreHardwareMonitor
start /min "" "LibreHardwareMonitor.exe"
cd ..

:: 2. Start Nexus Server (EXE)
start "" "Nexus-Server.exe"
