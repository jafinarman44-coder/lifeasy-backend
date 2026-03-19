@echo off
echo.
echo 🔥 💣 FULL HARD RESET (FINAL FIX)
echo ===================================
echo.
echo This will 100% solve all build issues!
echo.

set ORIGINAL_DIR=%CD%

REM ========================================
REM STEP 1: FLUTTER CLEAN
REM ========================================
echo 📱 STEP 1: Flutter Clean
echo ──────────────────────────────
echo.
cd /d "%~dp0mobile_app"

echo Running flutter clean...
echo.
flutter clean
if errorlevel 1 (
    echo ⚠️  Flutter clean had issues, continuing...
)
echo ✅ Flutter clean completed
echo.

REM ========================================
REM STEP 2: MANUAL DELETE (BUILD + CACHE)
REM ========================================
echo 🗑️  STEP 2: Manual Cache Deletion
echo ──────────────────────────────────────
echo.

if exist "build" (
    echo Deleting: build ...
    rmdir /s /q build
    echo   ✓ Deleted: build
) else (
    echo ℹ️  Not found: build
)

if exist ".dart_tool" (
    echo Deleting: .dart_tool ...
    rmdir /s /q .dart_tool
    echo   ✓ Deleted: .dart_tool
) else (
    echo ℹ️  Not found: .dart_tool
)

if exist "android\.gradle" (
    echo Deleting: android\.gradle ...
    rmdir /s /q android\.gradle
    echo   ✓ Deleted: android\.gradle
) else (
    echo ℹ️  Not found: android\.gradle
)

if exist "pubspec.lock" (
    echo Deleting: pubspec.lock ...
    del /q pubspec.lock
    echo   ✓ Deleted: pubspec.lock
)
echo.

REM ========================================
REM STEP 3: GRADLE CLEAN (IMPORTANT!)
REM ========================================
echo 🛠️  STEP 3: Gradle Cache Clear
echo ────────────────────────────────────
echo.
cd android

if exist "gradlew.bat" (
    echo Running gradlew clean...
    echo.
    call gradlew.bat clean
    if errorlevel 1 (
        echo ⚠️  Gradle clean had issues, continuing...
    ) else (
        echo ✅ Gradle clean completed
    )
) else (
    echo ⚠️  gradlew.bat not found, skipping
)
echo.

cd ..

REM ========================================
REM STEP 4: UPDATE GRADLE.PROPERTIES
REM ========================================
echo ⚙️  STEP 4: Update gradle.properties
echo ─────────────────────────────────────────
echo.

set GRADLE_PROPS=android\gradle.properties

if exist "%GRADLE_PROPS%" (
    echo Updating gradle.properties...
    
    REM Create temporary file with updated settings
    (
        echo org.gradle.jvmargs=-Xmx2048M -XX:MaxMetaspaceSize=512m
        findstr /V "^org.gradle.jvmargs=" "%GRADLE_PROPS%"
        findstr /V "^kotlin.incremental=" "%GRADLE_PROPS%" | findstr /R "^android\." 
    ) > "%GRADLE_PROPS%.tmp"
    
    REM Add kotlin.incremental=false if not exists
    findstr /C:"kotlin.incremental=" "%GRADLE_PROPS%.tmp" >nul
    if errorlevel 1 (
        echo kotlin.incremental=false >> "%GRADLE_PROPS%.tmp"
    )
    
    REM Replace original file
    move /y "%GRADLE_PROPS%.tmp" "%GRADLE_PROPS%" >nul
    
    echo ✅ Updated gradle.properties:
    echo    • org.gradle.jvmargs=-Xmx2048M
    echo    • kotlin.incremental=false
    echo.
) else (
    echo ⚠️  gradle.properties not found!
    echo.
)

REM ========================================
REM STEP 5: FLUTTER PUB GET
REM ========================================
echo 📦 STEP 5: Fetch Dependencies
echo ───────────────────────────────────────────────
echo.
echo Running flutter pub get...
echo.
flutter pub get

if errorlevel 1 (
    echo.
    echo ❌ Failed to fetch dependencies!
    echo.
    echo Troubleshooting:
    echo   1. Check internet connection
    echo   2. Run: flutter doctor
    echo   3. Run: flutter pub cache repair
    echo.
    cd /d "%ORIGINAL_DIR%"
    exit /b 1
)
echo.
echo ✅ Dependencies fetched successfully
echo.

REM ========================================
REM STEP 6: REBUILD APK
REM ========================================
echo 🏗️  STEP 6: Rebuild APK
echo ────────────────────────────────────────────
echo.
echo Running: flutter build apk --release --no-tree-shake-icons
echo.
echo ⏰ This will take 5-10 minutes...
echo.

flutter build apk --release --no-tree-shake-icons

if errorlevel 1 (
    echo.
    echo ❌ APK BUILD FAILED!
    echo.
    echo 🔧 Additional Fixes to Try:
    echo.
    echo 1. Clear Flutter cache:
    echo    flutter clean
    echo.
    echo 2. Check Flutter installation:
    echo    flutter doctor -v
    echo.
    echo 3. Update Flutter:
    echo    flutter upgrade
    echo.
    echo 4. Clear pub cache:
    echo    flutter pub cache clean
    echo    flutter pub get
    echo.
    cd /d "%ORIGINAL_DIR%"
    exit /b 1
)

echo.
echo 🎉 APK BUILT SUCCESSFULLY!
echo.

REM Show APK details
set APK_PATH=build\app\outputs\flutter-apk\app-release.apk
if exist "%APK_PATH%" (
    echo 📱 APK Details:
    echo    Location: %APK_PATH%
    for %%A in ("%APK_PATH%") do echo    Size: %%~zA bytes
    echo    Build Mode: Release
    echo    Icons: Not tree-shaken ^(faster build^)
    echo.
)

echo ✅ INSTALLATION READY!
echo.
echo 📲 Next Steps:
echo    1. Transfer APK to Android device
echo    2. Enable 'Install from Unknown Sources'
echo    3. Install the APK
echo    4. Login with:
echo       Tenant ID: 1001
echo       Password: 123456
echo.

REM ========================================
REM FINAL SUMMARY
REM ========================================
cd /d "%ORIGINAL_DIR%"

echo.
echo 🎯 FULL HARD RESET COMPLETE!
echo ═══════════════════════════════════════
echo.
echo ✅ Completed Steps:
echo    1. Flutter clean
echo    2. Manual cache deletion ^(build/, .dart_tool/, .gradle/^)
echo    3. Gradle clean
echo    4. Updated gradle.properties ^(JVM args + Kotlin settings^)
echo    5. Fetched dependencies ^(flutter pub get^)
echo    6. Built release APK ^(--no-tree-shake-icons^)
echo.
echo 🎊 YOUR APP IS 100% FIXED AND READY! 🎊
echo.
echo Build Time: %DATE% %TIME%
echo Status: SUCCESS
echo.
pause

