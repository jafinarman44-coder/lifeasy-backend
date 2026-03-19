# LIFEASY V28 ULTRA - APK Build Script
# Production Ready Mobile App Builder

$PROJECT = "E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27"

Write-Host ""
Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     LIFEASY V28 ULTRA - APK BUILD     ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

Set-Location "$PROJECT\mobile_app"

Write-Host "[1/5] Checking Flutter installation..." -ForegroundColor Yellow

flutter --version >$null 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Flutter not found!" -ForegroundColor Red
    Write-Host "Please install Flutter SDK and add to PATH" -ForegroundColor Gray
    pause
    exit 1
}

Write-Host "✓ Flutter ready" -ForegroundColor Green
Write-Host ""

Write-Host "[2/5] Cleaning project..." -ForegroundColor Yellow

flutter clean

Remove-Item ".dart_tool" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "build" -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "✓ Project cleaned" -ForegroundColor Green
Write-Host ""

Write-Host "[3/5] Configuring PUB_CACHE..." -ForegroundColor Yellow

$env:PUB_CACHE = "$PROJECT\.pub_cache"

if (!(Test-Path "$PROJECT\.pub_cache")) {
    New-Item -ItemType Directory -Path "$PROJECT\.pub_cache" | Out-Null
}

Write-Host "✓ PUB_CACHE configured" -ForegroundColor Green
Write-Host ""

Write-Host "[4/5] Getting dependencies..." -ForegroundColor Yellow

flutter pub get

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to get dependencies!" -ForegroundColor Red
    pause
    exit 1
}

Write-Host "✓ Dependencies installed" -ForegroundColor Green
Write-Host ""

Write-Host "[5/5] Building Release APK..." -ForegroundColor Yellow
Write-Host "This may take 3-5 minutes..." -ForegroundColor Gray
Write-Host ""

flutter build apk --release

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Red
    Write-Host "║         ✗ APK BUILD FAILED            ║" -ForegroundColor Red
    Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Red
    Write-Host ""
    Write-Host "Check the error messages above for details" -ForegroundColor Gray
    pause
    exit 1
}

# Verify APK was created
$APK_PATH = "$PROJECT\mobile_app\build\app\outputs\flutter-apk\app-release.apk"

Write-Host ""
Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║        ✓ APK BUILD SUCCESSFUL         ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

if (Test-Path $APK_PATH) {
    Write-Host "APK Location:" -ForegroundColor Cyan
    Write-Host $APK_PATH -ForegroundColor White
    Write-Host ""
    
    $fileSize = (Get-Item $APK_PATH).Length / 1MB
    Write-Host "File Size: $([math]::Round($fileSize, 2)) MB" -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "Next Steps:" -ForegroundColor Yellow
    Write-Host "1. Transfer APK to Android device" -ForegroundColor White
    Write-Host "2. Install the APK" -ForegroundColor White
    Write-Host "3. Test login with credentials:" -ForegroundColor White
    Write-Host "   Tenant ID: 1001" -ForegroundColor Gray
    Write-Host "   Password: 123456" -ForegroundColor Gray
} else {
    Write-Host "WARNING: APK file not found at expected location" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
