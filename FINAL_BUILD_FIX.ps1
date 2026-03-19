# ================================
# LIFEASY V27 FINAL BUILD FIX
# ================================

Write-Host "🔥 STEP 1: Killing Flutter/Gradle processes..." -ForegroundColor Cyan
taskkill /F /IM java.exe 2>$null
taskkill /F /IM gradle* 2>$null
Start-Sleep -Seconds 2

Write-Host "📁 STEP 2: Going to correct project..." -ForegroundColor Cyan
Set-Location "E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\mobile_app"

Write-Host "✅ STEP 3: Verifying Flutter project..." -ForegroundColor Cyan
if (!(Test-Path "pubspec.yaml")) {
    Write-Host "❌ ERROR: Not a Flutter project!" -ForegroundColor Red
    exit 1
} else {
    Write-Host "✓ Flutter project verified!" -ForegroundColor Green
}

Write-Host "🗑️  STEP 4: Deleting wrong build folders (SAFE)..." -ForegroundColor Cyan
Remove-Item -Recurse -Force build -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force .dart_tool -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force android\.gradle -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "..\mobile_app\tenant_app\build" -ErrorAction SilentlyContinue
Write-Host "✓ Cleanup complete!" -ForegroundColor Green

Write-Host "🧹 STEP 5: Flutter clean install..." -ForegroundColor Cyan
flutter clean
flutter pub get

Write-Host "⚙️  STEP 6: Fixing Gradle memory + Kotlin issue..." -ForegroundColor Cyan
Set-Content -Path "android\gradle.properties" -Value @"
org.gradle.jvmargs=-Xmx2048M
android.useAndroidX=true
android.enableJetifier=true
kotlin.incremental=false
"@
Write-Host "✓ Gradle properties updated!" -ForegroundColor Green

Write-Host "🏗️  STEP 7: Rebuilding APK (MAIN STEP)..." -ForegroundColor Yellow
flutter build apk --release --no-tree-shake-icons

Write-Host "✅ STEP 8: Verifying APK..." -ForegroundColor Cyan
if (Test-Path "build\app\outputs\flutter-apk\app-release.apk") {
    $apkSize = [math]::Round((Get-Item "build\app\outputs\flutter-apk\app-release.apk").Length / 1MB, 2)
    Write-Host "`n🎉 SUCCESS: APK BUILT HERE:" -ForegroundColor Green
    Write-Host "📍 E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\mobile_app\build\app\outputs\flutter-apk\app-release.apk" -ForegroundColor Yellow
    Write-Host "📦 Size: $apkSize MB`n" -ForegroundColor White
} else {
    Write-Host "`n❌ BUILD FAILED!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ ALL STEPS COMPLETE!" -ForegroundColor Green
