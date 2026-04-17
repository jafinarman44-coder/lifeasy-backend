# PowerShell Build Script
$mobileAppPath = "e:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\mobile_app"
$flutterPath = "E:\Flutter\flutter\bin\flutter.bat"

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  BUILDING FLUTTER APK" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Change to mobile app directory
Set-Location -LiteralPath $mobileAppPath
Write-Host "Working directory: $(Get-Location)" -ForegroundColor Yellow
Write-Host ""

# Step 1: Clean
Write-Host "[1/3] Cleaning project..." -ForegroundColor Yellow
& cmd.exe /c """$flutterPath"" clean"
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Clean failed!" -ForegroundColor Red
    pause
    exit 1
}
Write-Host ""

# Step 2: Pub get
Write-Host "[2/3] Getting dependencies..." -ForegroundColor Yellow
& cmd.exe /c """$flutterPath"" pub get"
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Dependencies failed!" -ForegroundColor Red
    pause
    exit 1
}
Write-Host ""

# Step 3: Build APK
Write-Host "[3/3] Building APK..." -ForegroundColor Yellow
Write-Host "This will take 3-5 minutes. Please wait..." -ForegroundColor Gray
& cmd.exe /c """$flutterPath"" build apk --release"
if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Build failed!" -ForegroundColor Red
    pause
    exit 1
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  BUILD SUCCESS!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "APK Location:" -ForegroundColor Yellow
Write-Host "$mobileAppPath\build\app\outputs\flutter-apk\app-release.apk" -ForegroundColor White
Write-Host ""
pause
