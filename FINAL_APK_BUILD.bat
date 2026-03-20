@echo off
echo ============================================================
echo FINAL APK BUILD - Release Mode
echo ============================================================
echo.

cd /d "e:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27"

powershell -ExecutionPolicy Bypass -File FINAL_APK_BUILD.ps1

echo.
echo Press any key to continue...
pause >nul
