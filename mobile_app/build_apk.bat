@echo off
echo === BUILDING APK ===
echo.

cd /d "e:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\mobile_app"

echo [1/3] Cleaning...
call flutter clean
echo.

echo [2/3] Getting dependencies...
call flutter pub get
echo.

echo [3/3] Building APK (this takes 3-5 minutes)...
call flutter build apk --release
echo.

if %ERRORLEVEL% EQU 0 (
    echo === BUILD SUCCESS ===
    echo APK Location: e:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\mobile_app\build\app\outputs\flutter-apk\app-release.apk
) else (
    echo === BUILD FAILED ===
)

pause
