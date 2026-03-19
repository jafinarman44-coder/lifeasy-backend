# ==========================================
# LIFEASY V28 ULTRA FINAL MASTER COMMAND
# ==========================================

$PROJECT="E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27"

Write-Host "====================================" -ForegroundColor Cyan
Write-Host " LIFEASY V28 ULTRA PRODUCTION SETUP " -ForegroundColor Cyan
Write-Host "====================================" -ForegroundColor Cyan
Write-Host ""

# ------------------------------------------
# STEP 1 - FIREWALL RULE
# ------------------------------------------

Write-Host "[STEP 1/7] Configuring firewall..." -ForegroundColor Yellow

netsh advfirewall firewall add rule name="FastAPI8000-IN" dir=in action=allow protocol=TCP localport=8000
netsh advfirewall firewall add rule name="FastAPI8000-OUT" dir=out action=allow protocol=TCP localport=8000

Write-Host "✓ Firewall rules configured" -ForegroundColor Green
Write-Host ""

# ------------------------------------------
# STEP 2 - START BACKEND SERVER
# ------------------------------------------

Write-Host "[STEP 2/7] Starting backend server..." -ForegroundColor Yellow

Start-Process powershell -ArgumentList "-NoExit","-Command","cd '$PROJECT\backend'; .\.venv\Scripts\Activate.ps1; python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload"

Write-Host "Waiting for backend to initialize..." -ForegroundColor Gray
Start-Sleep -Seconds 5

Write-Host "✓ Backend server started" -ForegroundColor Green
Write-Host ""

# ------------------------------------------
# STEP 3 - GO TO MOBILE APP & CLEAN
# ------------------------------------------

Write-Host "[STEP 3/7] Preparing mobile app project..." -ForegroundColor Yellow

Set-Location "$PROJECT\mobile_app"

Write-Host "Cleaning flutter project..." -ForegroundColor Gray

flutter clean

Remove-Item ".dart_tool" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "build" -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "✓ Project cleaned" -ForegroundColor Green
Write-Host ""

# ------------------------------------------
# STEP 4 - FIX PUB CACHE DRIVE ERROR
# ------------------------------------------

Write-Host "[STEP 4/7] Configuring PUB_CACHE..." -ForegroundColor Yellow

$env:PUB_CACHE="$PROJECT\.pub_cache"

if (!(Test-Path "$PROJECT\.pub_cache")) {
    New-Item -ItemType Directory -Path "$PROJECT\.pub_cache" | Out-Null
}

flutter pub get

Write-Host "✓ Dependencies fetched" -ForegroundColor Green
Write-Host ""

# ------------------------------------------
# STEP 5 - CREATE BUILD DIRECTORY
# ------------------------------------------

Write-Host "[STEP 5/7] Creating build directory..." -ForegroundColor Yellow

if (!(Test-Path "build")) {
    New-Item -ItemType Directory -Path "build" | Out-Null
}

Write-Host "✓ Build directory ready" -ForegroundColor Green
Write-Host ""

# ------------------------------------------
# STEP 6 - BUILD RELEASE APK
# ------------------------------------------

Write-Host "[STEP 6/7] Building release APK..." -ForegroundColor Yellow
Write-Host "This may take several minutes..." -ForegroundColor Gray
Write-Host ""

flutter build apk --release

# ------------------------------------------
# STEP 7 - VERIFY APK
# ------------------------------------------

Write-Host ""
Write-Host "[STEP 7/7] Verifying APK build..." -ForegroundColor Yellow

$APK="$PROJECT\mobile_app\build\app\outputs\flutter-apk\app-release.apk"

if (Test-Path $APK){
    Write-Host ""
    Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║   ✓ APK BUILD SUCCESSFUL              ║" -ForegroundColor Green
    Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host ""
    Write-Host "APK LOCATION:" -ForegroundColor Cyan
    Write-Host $APK -ForegroundColor White
    Write-Host ""
    Write-Host "File size: $((Get-Item $APK).Length / 1MB) MB" -ForegroundColor Gray

} else {
    Write-Host ""
    Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Red
    Write-Host "║   ✗ APK BUILD FAILED                  ║" -ForegroundColor Red
    Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Red
    Write-Host ""
}

# ------------------------------------------
# FINAL SUMMARY
# ------------------------------------------

Write-Host ""
Write-Host "═══════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "     LIFEASY V28 ULTRA SETUP COMPLETE      " -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""
Write-Host "Backend API Documentation:" -ForegroundColor Yellow
Write-Host "  • Local:    http://localhost:8000/docs" -ForegroundColor White
Write-Host "  • Network:  http://192.168.0.119:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "Test Credentials:" -ForegroundColor Yellow
Write-Host "  Tenant ID:  1001" -ForegroundColor White
Write-Host "  Password:   123456" -ForegroundColor White
Write-Host "  OTP Code:   123456" -ForegroundColor White
Write-Host ""
Write-Host "Mobile App:" -ForegroundColor Yellow
Write-Host "  Install APK on Android device for testing" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
