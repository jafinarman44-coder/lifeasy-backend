@echo off
echo ========================================
echo LAUNCHING LIFEASY MOBILE APP
echo ========================================
echo.

cd /d "E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\mobile_app"

echo [1/3] Cleaning...
call flutter clean
echo ✅ Clean complete!
echo.

echo [2/3] Restoring files...
call flutter create .
echo ✅ Files restored!
echo.

echo [3/3] Getting dependencies...
call flutter pub get
echo ✅ Dependencies installed!
echo.

echo ========================================
echo 🚀 LAUNCHING ON WINDOWS...
echo ========================================
echo.
echo The app will launch shortly!
echo Watch for the Lifeasy window to appear.
echo.
echo Press Ctrl+C to stop the app.
echo.

flutter run -d windows

pause
