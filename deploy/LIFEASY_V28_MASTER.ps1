# ==========================================
# LIFEASY V28 ULTRA FINAL MASTER COMMAND
# Real Production Ready System
# ==========================================

$PROJECT = "E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27"

Write-Host ""
Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   LIFEASY V28 ULTRA PRODUCTION SETUP  ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# ------------------------------------------
# STEP 1 - FIREWALL RULE (Admin Required)
# ------------------------------------------

Write-Host "[STEP 1/6] Configuring Windows Firewall..." -ForegroundColor Yellow

try {
    netsh advfirewall firewall add rule name="FastAPI8000-IN" dir=in action=allow protocol=TCP localport=8000
    netsh advfirewall firewall add rule name="FastAPI8000-OUT" dir=out action=allow protocol=TCP localport=8000
    Write-Host "✓ Firewall rules configured" -ForegroundColor Green
} catch {
    Write-Host "⚠ Firewall configuration failed - Run as Administrator!" -ForegroundColor Red
    Write-Host "Right-click this script → Run as Administrator" -ForegroundColor Gray
}

Write-Host ""

# ------------------------------------------
# STEP 2 - START BACKEND SERVER
# ------------------------------------------

Write-Host "[STEP 2/6] Starting Backend Server..." -ForegroundColor Yellow

Start-Process powershell -ArgumentList "-NoExit", "-Command", @"
cd '$PROJECT\deploy'; .\start_backend.ps1
"@

Write-Host "Waiting for backend to initialize..." -ForegroundColor Gray
Start-Sleep -Seconds 5

Write-Host "✓ Backend server started in new window" -ForegroundColor Green
Write-Host ""

# ------------------------------------------
# STEP 3 - VERIFY API ACCESSIBILITY
# ------------------------------------------

Write-Host "[STEP 3/6] Verifying API accessibility..." -ForegroundColor Yellow

Start-Sleep -Seconds 3

try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/health" -TimeoutSec 3 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✓ Backend API is accessible" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠ Backend not responding yet - continuing..." -ForegroundColor Yellow
}

Write-Host ""

# ------------------------------------------
# STEP 4 - PREPARE MOBILE APP
# ------------------------------------------

Write-Host "[STEP 4/6] Preparing Mobile App Project..." -ForegroundColor Yellow

Set-Location "$PROJECT\mobile_app"

Write-Host "Cleaning Flutter project..." -ForegroundColor Gray

flutter clean >$null 2>&1

Remove-Item ".dart_tool" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "build" -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "✓ Project cleaned" -ForegroundColor Green
Write-Host ""

# ------------------------------------------
# STEP 5 - CONFIGURE DEPENDENCIES
# ------------------------------------------

Write-Host "[STEP 5/6] Configuring Dependencies..." -ForegroundColor Yellow

$env:PUB_CACHE = "$PROJECT\.pub_cache"

if (!(Test-Path "$PROJECT\.pub_cache")) {
    New-Item -ItemType Directory -Path "$PROJECT\.pub_cache" | Out-Null
}

Write-Host "Getting Flutter packages..." -ForegroundColor Gray

flutter pub get

if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠ Package installation had issues" -ForegroundColor Yellow
} else {
    Write-Host "✓ Dependencies configured" -ForegroundColor Green
}

Write-Host ""

# ------------------------------------------
# STEP 6 - BUILD RELEASE APK
# ------------------------------------------

Write-Host "[STEP 6/6] Building Release APK..." -ForegroundColor Yellow
Write-Host "This will take 3-5 minutes..." -ForegroundColor Gray
Write-Host ""

flutter build apk --release

# ------------------------------------------
# FINAL VERIFICATION
# ------------------------------------------

$APK = "$PROJECT\mobile_app\build\app\outputs\flutter-apk\app-release.apk"

Write-Host ""
Write-Host "═══════════════════════════════════════════" -ForegroundColor Cyan

if (Test-Path $APK) {
    Write-Host "     ✓ LIFEASY V28 ULTRA READY" -ForegroundColor Green
    Write-Host "═══════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "📦 APK Location:" -ForegroundColor Yellow
    Write-Host $APK -ForegroundColor White
    Write-Host ""
    
    $fileSize = (Get-Item $APK).Length / 1MB
    Write-Host "File Size: $([math]::Round($fileSize, 2)) MB" -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "🌐 Backend API:" -ForegroundColor Yellow
    Write-Host "  • Local:   http://localhost:8000/docs" -ForegroundColor White
    Write-Host "  • Network: http://192.168.0.119:8000/docs" -ForegroundColor White
    Write-Host ""
    
    Write-Host "📱 Test Login Credentials:" -ForegroundColor Yellow
    Write-Host "  Tenant ID:  1001" -ForegroundColor White
    Write-Host "  Password:   123456" -ForegroundColor White
    Write-Host "  OTP Code:   Will be generated on login" -ForegroundColor White
    Write-Host ""
    
    Write-Host "✅ Next Steps:" -ForegroundColor Green
    Write-Host "  1. Install APK on Android device" -ForegroundColor White
    Write-Host "  2. Ensure device is on same WiFi network" -ForegroundColor White
    Write-Host "  3. Login with credentials above" -ForegroundColor White
    Write-Host "  4. Enter OTP when received" -ForegroundColor White
    
} else {
    Write-Host "     ⚠ BUILD INCOMPLETE" -ForegroundColor Red
    Write-Host "═══════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "APK file not found. Check build errors above." -ForegroundColor Yellow
    Write-Host "Backend server should still be running." -ForegroundColor Gray
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
