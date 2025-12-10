@echo off
cd /d "%~dp0"

:: Start LibreHardwareMonitor normally
cd LibreHardwareMonitor
start "" "LibreHardwareMonitor.exe"
cd ..

:: Run server.py directly with logs (only if server.py is present here)
python server.py
pause
