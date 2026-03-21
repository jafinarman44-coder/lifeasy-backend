@echo off
echo ============================================================
echo REAL PRODUCTION BACKEND - MASTER SETUP
echo Professional Structure (NOT Demo Code)
echo ============================================================
echo.

cd /d "e:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27"

powershell -ExecutionPolicy Bypass -File REAL_PRODUCTION_BACKEND.ps1

echo.
echo ============================================================
echo NEXT STEPS:
echo ============================================================
echo.
echo git commit -m "REAL PRODUCTION BACKEND STRUCTURE"
echo git push origin main --force
echo.
pause
