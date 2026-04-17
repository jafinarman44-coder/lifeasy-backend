# BUILD APK WITH E: DRIVE - Solves C: drive space issue
Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║     BUILDING APK WITH E: DRIVE (No C: Space Needed)    ║" -ForegroundColor Green
Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""

# Set all Flutter/Dart temp and cache to E: drive
Write-Host "[1/5] Setting environment variables to E: drive..." -ForegroundColor Yellow
$env:TEMP = "E:\temp"
$env:TMP = "E:\temp"
$env:PUB_CACHE = "E:\.pub-cache"
$env:ANDROID_SDK_HOME = "E:\Android\Sdk"

# Create temp directories on E: drive
if (-not (Test-Path "E:\temp")) {
    New-Item -ItemType Directory -Path "E:\temp" | Out-Null
}
if (-not (Test-Path "E:\.pub-cache")) {
    New-Item -ItemType Directory -Path "E:\.pub-cache" | Out-Null
}

Write-Host "  ✓ All temp/cache dirs set to E: drive" -ForegroundColor Green
Write-Host ""

# Navigate to mobile app
Write-Host "[2/5] Navigating to mobile app..." -ForegroundColor Yellow
Set-Location "$PSScriptRoot"
Write-Host "  ✓ Location: $(Get-Location)" -ForegroundColor Green
Write-Host ""

# Clean Flutter
Write-Host "[3/5] Cleaning Flutter project..." -ForegroundColor Yellow
try {
    & "E:\Flutter\flutter\bin\flutter.bat" clean
    Write-Host "  ✓ Flutter clean completed" -ForegroundColor Green
} catch {
    Write-Host "  ⚠ Clean had warnings (normal)" -ForegroundColor Yellow
}
Write-Host ""

# Get dependencies
Write-Host "[4/5] Getting dependencies..." -ForegroundColor Yellow
try {
    & "E:\Flutter\flutter\bin\flutter.bat" pub get
    Write-Host "  ✓ Dependencies downloaded" -ForegroundColor Green
} catch {
    Write-Host "  ✗ Pub get failed" -ForegroundColor Red
    exit 1
}
Write-Host ""

# Build APK
Write-Host "[5/5] Building APK..." -ForegroundColor Yellow
Write-Host "This may take 10-15 minutes..." -ForegroundColor Cyan
Write-Host ""
try {
    & "E:\Flutter\flutter\bin\flutter.bat" build apk --release
    Write-Host ""
    Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Green
    Write-Host "║           APK BUILD SUCCESSFUL!                          ║" -ForegroundColor Green
    Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Green
    Write-Host ""
    
    # Find APK
    $apkPath = "build\app\outputs\flutter-apk\app-release.apk"
    if (Test-Path $apkPath) {
        $size = (Get-Item $apkPath).Length / 1MB
        Write-Host "APK Location: $(Resolve-Path $apkPath)" -ForegroundColor Cyan
        Write-Host "APK Size: $([math]::Round($size, 2)) MB" -ForegroundColor Cyan
        Write-Host ""
    }
} catch {
    Write-Host "  ✗ APK build failed!" -ForegroundColor Red
    exit 1
}
