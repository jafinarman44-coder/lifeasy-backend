@echo off
echo ============================================================
echo MASTER FIX - MOVE main_prod.py TO ROOT
echo 100%% WORKING - Clean Production Backend
echo ============================================================
echo.

cd /d "e:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27"

powershell -ExecutionPolicy Bypass -File MASTER_FIX_MOVE_TO_ROOT.ps1

echo.
echo Press any key to continue...
pause >nul
