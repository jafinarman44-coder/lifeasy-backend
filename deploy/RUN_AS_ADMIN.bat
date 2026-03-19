@echo off
:: LIFEASY V28 ULTRA - Auto-Admin Launcher
:: Automatically requests administrator privileges

echo ====================================
echo  LIFEASY V28 ULTRA SETUP LAUNCHER
echo ====================================
echo.

:: Check admin rights
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running as Administrator...
    goto :RUN
)

echo Requesting Administrator access...
echo.

:: Create elevation script
echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\elevate.vbs"
echo UAC.ShellExecute "cmd.exe", "/c ""%~dpnx0""", "", "runas", 1 >> "%temp%\elevate.vbs"

cscript //nologo "%temp%\elevate.vbs"
del "%temp%\elevate.vbs"
exit /b

:RUN
echo.
echo Starting LIFEASY V28 ULTRA Production Setup...
echo.

powershell -NoProfile -ExecutionPolicy Bypass -File "E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\deploy\LIFEASY_V28_MASTER.ps1"

echo.
pause
