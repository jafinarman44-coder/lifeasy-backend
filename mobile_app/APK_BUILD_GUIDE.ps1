# LIFEASY - Flutter APK Build Guide
# Manual steps to build the APK

Write-Host ""
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host "   LIFEASY - ANDROID APK BUILD GUIDE" -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan
Write-Host ""

$projectPath = "e:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\mobile_app"
$flutterPath = "E:\Flutter\flutter\bin"

Write-Host "📱 PROJECT INFORMATION" -ForegroundColor Yellow
Write-Host "   Mobile App: $projectPath" -ForegroundColor White
Write-Host "   Flutter SDK: $flutterPath" -ForegroundColor White
Write-Host ""

Write-Host "⚠️  IMPORTANT: Flutter Path Issue Detected!" -ForegroundColor Red
Write-Host ""
Write-Host "The Flutter installation at E:\Flutter\flutter has path configuration issues." -ForegroundColor Yellow
Write-Host ""

Write-Host "════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "   SOLUTION: REBUILD FLUTTER SDK" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

Write-Host "Follow these steps to fix and build the APK:" -ForegroundColor Yellow
Write-Host ""

Write-Host "STEP 1: Reinstall Flutter SDK" -ForegroundColor Green
Write-Host "---------------------------------------------------" -ForegroundColor Gray
Write-Host "1. Download fresh Flutter SDK from:" -ForegroundColor White
Write-Host "   https://docs.flutter.dev/get-started/install/windows" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. Extract to: C:\src\flutter" -ForegroundColor White
Write-Host "   (Make sure the path has NO spaces)" -ForegroundColor Yellow
Write-Host ""

Write-Host "STEP 2: Add Flutter to System PATH" -ForegroundColor Green
Write-Host "---------------------------------------------------" -ForegroundColor Gray
Write-Host "1. Press Windows + R" -ForegroundColor White
Write-Host "2. Type: sysdm.cpl and press Enter" -ForegroundColor White
Write-Host "3. Click 'Advanced' tab" -ForegroundColor White
Write-Host "4. Click 'Environment Variables'" -ForegroundColor White
Write-Host "5. Under 'User variables', find and select 'Path'" -ForegroundColor White
Write-Host "6. Click 'Edit'" -ForegroundColor White
Write-Host "7. Click 'New' and add: C:\src\flutter\bin" -ForegroundColor White
Write-Host "8. Click 'OK' on all windows" -ForegroundColor White
Write-Host ""

Write-Host "STEP 3: Restart and Verify" -ForegroundColor Green
Write-Host "---------------------------------------------------" -ForegroundColor Gray
Write-Host "1. CLOSE this PowerShell window" -ForegroundColor White
Write-Host "2. Open a NEW PowerShell window" -ForegroundColor White
Write-Host "3. Run: flutter --version" -ForegroundColor White
Write-Host "4. You should see Flutter version information" -ForegroundColor White
Write-Host ""

Write-Host "STEP 4: Install Android Studio (if not installed)" -ForegroundColor Green
Write-Host "---------------------------------------------------" -ForegroundColor Gray
Write-Host "1. Download from: https://developer.android.com/studio" -ForegroundColor Cyan
Write-Host "2. Install Android Studio" -ForegroundColor White
Write-Host "3. Open Android Studio" -ForegroundColor White
Write-Host "4. Go to Settings > Android SDK" -ForegroundColor White
Write-Host "5. Install Android SDK (API 34 recommended)" -ForegroundColor White
Write-Host ""

Write-Host "STEP 5: Accept Android Licenses" -ForegroundColor Green
Write-Host "---------------------------------------------------" -ForegroundColor Gray
Write-Host "Run in PowerShell:" -ForegroundColor White
Write-Host "   flutter doctor --android-licenses" -ForegroundColor Cyan
Write-Host "   (Type 'y' to accept all)" -ForegroundColor Yellow
Write-Host ""

Write-Host "STEP 6: Build APK" -ForegroundColor Green
Write-Host "---------------------------------------------------" -ForegroundColor Gray
Write-Host "Navigate to your project and build:" -ForegroundColor White
Write-Host ""
Write-Host "   cd `"$projectPath`"" -ForegroundColor Cyan
Write-Host "   flutter clean" -ForegroundColor Cyan
Write-Host "   flutter pub get" -ForegroundColor Cyan
Write-Host "   flutter build apk --release" -ForegroundColor Cyan
Write-Host ""

Write-Host "════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "   QUICK BUILD COMMANDS (After fixing Flutter)" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "Copy and paste these commands in a NEW PowerShell window:" -ForegroundColor Yellow
Write-Host ""

Write-Host "# Command 1: Navigate to project" -ForegroundColor Green
Write-Host "cd `"$projectPath`"" -ForegroundColor White
Write-Host ""

Write-Host "# Command 2: Clean old builds" -ForegroundColor Green
Write-Host "flutter clean" -ForegroundColor White
Write-Host ""

Write-Host "# Command 3: Get dependencies" -ForegroundColor Green
Write-Host "flutter pub get" -ForegroundColor White
Write-Host ""

Write-Host "# Command 4: Build APK" -ForegroundColor Green
Write-Host "flutter build apk --release" -ForegroundColor White
Write-Host ""

Write-Host "════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "   APK OUTPUT LOCATION (After successful build)" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "The APK will be at:" -ForegroundColor Yellow
Write-Host "$projectPath\build\app\outputs\flutter-apk\app-release.apk" -ForegroundColor Cyan
Write-Host ""

Write-Host "════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "   ALTERNATIVE: Use Existing Build Script" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "After fixing Flutter, you can also run:" -ForegroundColor Yellow
Write-Host "   cd `"$projectPath`"" -ForegroundColor Cyan
Write-Host "   powershell -ExecutionPolicy Bypass -File BUILD_APK_STEP_BY_STEP.ps1" -ForegroundColor Cyan
Write-Host ""

Write-Host "Press any key to exit..."
pause
