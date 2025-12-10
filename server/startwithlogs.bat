@echo off
cd /d "%~dp0"

:: 1. Start LibreHardwareMonitor
cd LibreHardwareMonitor
start "" "LibreHardwareMonitor.exe"
cd ..

:: 2. Start Python Server
python server.py
