# Simple build script
$ErrorActionPreference = "Stop"

Write-Host "=== FLUTTER BUILD START ===" -ForegroundColor Cyan

# Set Flutter path
$env:Path = "E:\Flutter\flutter\bin;" + $env:Path

# Navigate to mobile app
Set-Location -LiteralPath "e:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\mobile_app"

# Clean
Write-Host "`n[1/3] Cleaning..." -ForegroundColor Yellow
flutter clean

# Get dependencies  
Write-Host "`n[2/3] Getting dependencies..." -ForegroundColor Yellow
flutter pub get

# Build
Write-Host "`n[3/3] Building APK..." -ForegroundColor Yellow
flutter build apk --release

Write-Host "`n=== BUILD COMPLETE ===" -ForegroundColor Green
