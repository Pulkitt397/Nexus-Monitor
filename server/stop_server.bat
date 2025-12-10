... (Admin check part stays same) ...

:run_kill
echo Stopping Nexus Monitor...
taskkill /F /IM Nexus-Server.exe
taskkill /F /IM LibreHardwareMonitor.exe
echo.
echo All processes stopped.
pause
