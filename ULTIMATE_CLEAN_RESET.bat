@echo off
echo ============================================================
echo ULTIMATE CLEAN RESET - GITHUB PURGE
echo NO MORE CONFUSION - CLEAN ROOT BACKEND ONLY
echo ============================================================
echo.

cd /d "e:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27"

powershell -ExecutionPolicy Bypass -File ULTIMATE_CLEAN_RESET.ps1

echo.
echo ============================================================
echo READY TO COMMIT! Run these commands now:
echo ============================================================
echo.
echo git commit -m "CLEAN ROOT BACKEND ONLY"
echo git push origin main
echo.
pause
