@echo off
:: LIFEASY V28 ULTRA - Auto-Elevate to Administrator
:: This batch file will request admin rights and run the PowerShell script

echo ====================================
echo  LIFEASY V28 ULTRA SETUP LAUNCHER
echo ====================================
echo.

:: Check if running as administrator
net session >nul 2>&1
if %errorLevel% == 0 (
    echo Running as Administrator...
    goto :RUN_SCRIPT
)

echo Requesting Administrator privileges...
echo.

:: Create temporary VBScript to elevate
set "batchPath=%~dpnx0"
set params=%*
if defined params set params=%params:"=\"%

echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\elevate.vbs"
echo UAC.ShellExecute "cmd.exe", "/c ""%batchPath%"" %params%", "", "runas", 1 >> "%temp%\elevate.vbs"

:: Run elevation script
cscript //nologo "%temp%\elevate.vbs"

:: Clean up
del "%temp%\elevate.vbs"

:: Exit current non-elevated process
exit /b

:RUN_SCRIPT
echo.
echo Starting LIFEASY V28 ULTRA Master Setup...
echo.

:: Run the PowerShell script
powershell -NoProfile -ExecutionPolicy Bypass -File "E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\LIFEASY_V28_ULTRA_MASTER.ps1"

echo.
echo Press any key to exit...
pause >nul
