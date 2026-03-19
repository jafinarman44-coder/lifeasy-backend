@echo off
echo ================================
echo LIFEASY V27 FINAL BUILD FIX
echo ================================
echo.

echo STEP 1: Killing Flutter/Gradle processes...
taskkill /F /IM java.exe 2>nul
taskkill /F /IM gradle* 2>nul
timeout /t 3 /nobreak >nul
echo.

echo STEP 2: Going to correct project...
cd /d "E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\mobile_app"
echo Current directory: %CD%
echo.

echo STEP 3: Verifying Flutter project...
if not exist "pubspec.yaml" (
    echo ERROR: Not a Flutter project!
    pause
    exit /b 1
)
echo Flutter project verified!
echo.

echo STEP 4: Deleting wrong build folders (SAFE)...
rmdir /s /q build 2>nul
rmdir /s /q .dart_tool 2>nul
rmdir /s /q android\.gradle 2>nul
echo Cleanup complete!
echo.

echo STEP 5: Flutter clean install...
flutter clean
flutter pub get
echo.

echo STEP 6: Fixing Gradle memory + Kotlin issue...
(
echo org.gradle.jvmargs=-Xmx2048M
echo android.useAndroidX=true
echo android.enableJetifier=true
echo kotlin.incremental=false
) > android\gradle.properties
echo Gradle properties updated!
echo.

echo STEP 7: Rebuilding APK (MAIN STEP)...
flutter build apk --release --no-tree-shake-icons
echo.

echo STEP 8: Verifying APK...
if exist "build\app\outputs\flutter-apk\app-release.apk" (
    echo.
    echo SUCCESS: APK BUILT HERE:
    echo E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\mobile_app\build\app\outputs\flutter-apk\app-release.apk
    echo.
) else (
    echo.
    echo BUILD FAILED!
    echo.
)

pause
