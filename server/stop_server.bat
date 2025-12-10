@echo off
echo Stopping Nexus Server and LibreHardwareMonitor...
taskkill /F /IM Nexus-Server.exe >nul 2>&1
taskkill /F /IM LibreHardwareMonitor.exe >nul 2>&1
echo Done.
pause
