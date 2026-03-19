@echo off
echo.
echo 🚀 FINAL CLEAN FLOW (WORKING)
echo ==============================
echo.

REM 🔥 BACKEND SETUP
echo 🔥 BACKEND
echo ============
cd /d "%~dp0backend"

echo.
echo 🗑️  Cleaning old database files...
del *.db /Q

echo.
echo 🌱 Running seed_prod.py...
python seed_prod.py
if errorlevel 1 (
    echo ❌ Database seeding failed!
    pause
    exit /b 1
)
echo ✅ Database seeded successfully!

echo.
echo 🚀 Starting backend server...
echo ⚠️  This will run in background. Press Ctrl+C to stop later.
start "LIFEASY Backend" python -m uvicorn main_prod:app --host 0.0.0.0 --port 8000

echo ✅ Backend server started on http://0.0.0.0:8000
echo.
echo ⏳ Waiting for backend to initialize...
timeout /t 5 /nobreak >nul

REM 🔥 MOBILE APP BUILD
echo.
echo 🔥 MOBILE APP BUILD
echo ===================
cd ..\mobile_app

echo.
echo 🧹 Running flutter clean...
flutter clean

echo.
echo 📦 Running flutter pub get...
flutter pub get

echo.
echo 🏗️  Building APK (Release Mode)...
echo ⏰ This will take 5-10 minutes...
echo.
flutter build apk --release

if errorlevel 1 (
    echo.
    echo ❌ APK build failed!
    echo.
    echo Troubleshooting tips:
    echo    1. Check Flutter installation: flutter doctor
    echo    2. Ensure Android SDK is configured
    echo    3. Check error messages above
    pause
    exit /b 1
)

echo.
echo ✅ APK built successfully!

REM Show APK details
set APK_PATH=build\app\outputs\flutter-apk\app-release.apk
if exist "%APK_PATH%" (
    echo.
    echo 📱 APK Details:
    echo    Location: %APK_PATH%
    for %%A in ("%APK_PATH%") do echo    Size: %%~zA bytes
)

echo.
echo 🎉 BUILD COMPLETE!
echo.
echo 📲 Installation Instructions:
echo    1. Transfer APK to Android device
echo    2. Enable 'Install from Unknown Sources'
echo    3. Install and open the app
echo    4. Login with credentials:
echo       Tenant ID: 1001
echo       Password: 123456
echo.

echo 🎯 FINAL STATUS
echo ==============
echo ✅ Backend: Running on http://0.0.0.0:8000
echo ✅ Mobile APK: Built successfully
echo ✅ Authentication: Direct login (OTP removed)
echo.
echo 🎊 LIFEASY V27 READY FOR DEPLOYMENT! 🎊
echo.
pause
