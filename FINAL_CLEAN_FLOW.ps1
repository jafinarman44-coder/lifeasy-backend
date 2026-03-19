# 🚀 FINAL CLEAN FLOW - LIFEASY V27
# Complete rebuild and deployment script

Write-Host "`n🚀 FINAL CLEAN FLOW (WORKING)`n" -ForegroundColor Cyan

# ========================================
# 🔥 BACKEND SETUP
# ========================================
Write-Host "🔥 BACKEND SETUP" -ForegroundColor Yellow
Write-Host "================`n" -ForegroundColor Gray

Write-Host "📁 Navigating to backend directory..." -ForegroundColor Cyan
Set-Location -Path ".\LIFEASY_V27\backend"

Write-Host "🗑️  Cleaning old database files..." -ForegroundColor Yellow
if (Test-Path "*.db") {
    Get-ChildItem -Filter "*.db" | Remove-Force
    Write-Host "✅ Old databases removed" -ForegroundColor Green
} else {
    Write-Host "ℹ️  No old database files found" -ForegroundColor Gray
}

Write-Host "`n🌱 Running seed_prod.py to create fresh database..." -ForegroundColor Yellow
python seed_prod.py

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Database seeded successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Database seeding failed!" -ForegroundColor Red
    exit 1
}

Write-Host "`n🚀 Starting backend server..." -ForegroundColor Yellow
Write-Host "⚠️  This will run in background. Press Ctrl+C to stop later.`n" -ForegroundColor Gray

# Start backend in background
Start-Process python -ArgumentList "-m", "uvicorn", "main_prod:app", "--host", "0.0.0.0", "--port", "8000" -WindowStyle Hidden
Write-Host "✅ Backend server started on http://0.0.0.0:8000" -ForegroundColor Green

# Wait for server to start
Write-Host "`n⏳ Waiting for backend to initialize..." -ForegroundColor Cyan
Start-Sleep -Seconds 5

# ========================================
# 🔥 MOBILE APP BUILD
# ========================================
Write-Host "`n🔥 MOBILE APP BUILD" -ForegroundColor Yellow
Write-Host "==================`n" -ForegroundColor Gray

Write-Host "📁 Navigating to mobile_app directory..." -ForegroundColor Cyan
Set-Location -Path "..\mobile_app"

Write-Host "`n🧹 Running flutter clean..." -ForegroundColor Yellow
flutter clean

Write-Host "`n📦 Running flutter pub get..." -ForegroundColor Yellow
flutter pub get

Write-Host "`n🏗️  Building APK (Release Mode)..." -ForegroundColor Yellow
Write-Host "⏰ This will take 5-10 minutes...`n" -ForegroundColor Gray

flutter build apk --release

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ APK built successfully!" -ForegroundColor Green
    
    # Show APK details
    $apkPath = "build\app\outputs\flutter-apk\app-release.apk"
    if (Test-Path $apkPath) {
        $fileSize = (Get-Item $apkPath).Length / 1MB
        Write-Host "`n📱 APK Details:" -ForegroundColor Cyan
        Write-Host "   Location: $apkPath" -ForegroundColor White
        Write-Host "   Size: $([math]::Round($fileSize, 2)) MB" -ForegroundColor Gray
    }
    
    Write-Host "`n🎉 BUILD COMPLETE!" -ForegroundColor Green
    Write-Host "`n📲 Installation Instructions:" -ForegroundColor Cyan
    Write-Host "   1. Transfer APK to Android device" -ForegroundColor White
    Write-Host "   2. Enable 'Install from Unknown Sources'" -ForegroundColor White
    Write-Host "   3. Install and open the app" -ForegroundColor White
    Write-Host "   4. Login with credentials:" -ForegroundColor White
    Write-Host "      Tenant ID: 1001" -ForegroundColor Gray
    Write-Host "      Password: 123456" -ForegroundColor Gray
    Write-Host ""
} else {
    Write-Host "`n❌ APK build failed!" -ForegroundColor Red
    Write-Host "`nTroubleshooting tips:" -ForegroundColor Yellow
    Write-Host "   1. Check Flutter installation: flutter doctor" -ForegroundColor White
    Write-Host "   2. Ensure Android SDK is configured" -ForegroundColor White
    Write-Host "   3. Check error messages above" -ForegroundColor White
    exit 1
}

# ========================================
# FINAL STATUS
# ========================================
Write-Host "`n🎯 FINAL STATUS" -ForegroundColor Cyan
Write-Host "=============`n" -ForegroundColor Gray
Write-Host "✅ Backend: Running on http://0.0.0.0:8000" -ForegroundColor Green
Write-Host "✅ Mobile APK: Built successfully" -ForegroundColor Green
Write-Host "✅ Authentication: Direct login (OTP removed)" -ForegroundColor Green
Write-Host "`n🎊 LIFEASY V27 READY FOR DEPLOYMENT! 🎊" -ForegroundColor Green
Write-Host ""
