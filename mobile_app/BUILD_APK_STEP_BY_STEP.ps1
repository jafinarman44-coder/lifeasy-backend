# LIFEASY V28 - Flutter Mobile App Build Script
# Step-by-step verification and APK builder

$PROJECT = "E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27"

Write-Host ""
Write-Host "╔══════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   LIFEASY V28 - MOBILE APP BUILD PROCESS    ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

Set-Location "$PROJECT\mobile_app"

# ==========================================
# STEP 1 - PROJECT STRUCTURE VERIFICATION
# ==========================================

Write-Host "[STEP 1/5] Verifying Project Structure..." -ForegroundColor Yellow
Write-Host ""

$requiredFolders = @("android", "ios", "lib")
$requiredFiles = @("pubspec.yaml")

$allGood = $true

foreach ($folder in $requiredFolders) {
    if (Test-Path $folder) {
        Write-Host "  ✓ $folder folder found" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $folder folder MISSING!" -ForegroundColor Red
        $allGood = $false
    }
}

foreach ($file in $requiredFiles) {
    if (Test-Path $file) {
        Write-Host "  ✓ $file file found" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $file file MISSING!" -ForegroundColor Red
        $allGood = $false
    }
}

Write-Host ""

if (!$allGood) {
    Write-Host "ERROR: Project structure is incomplete!" -ForegroundColor Red
    Write-Host "Please ensure you're in the correct Flutter project directory." -ForegroundColor Gray
    pause
    exit 1
}

Write-Host "✓ Flutter project structure verified!" -ForegroundColor Green
Write-Host ""

# ==========================================
# STEP 2 - FLUTTER ENVIRONMENT CHECK
# ==========================================

Write-Host "[STEP 2/5] Checking Flutter Environment..." -ForegroundColor Yellow
Write-Host ""

flutter --version

Write-Host ""
Write-Host "Running flutter doctor..." -ForegroundColor Gray
Write-Host "(This checks your Flutter installation)" -ForegroundColor Gray
Write-Host ""

flutter doctor -v

Write-Host ""
Write-Host "⚠ Check the output above:" -ForegroundColor Yellow
Write-Host "  • All items should have ✓ marks" -ForegroundColor White
Write-Host "  • Android toolchain should be OK" -ForegroundColor White
Write-Host "  • No critical issues allowed" -ForegroundColor White
Write-Host ""

$userResponse = Read-Host "Is flutter doctor showing all green checks? (y/n)"

if ($userResponse -ne "y" -and $userResponse -ne "Y") {
    Write-Host ""
    Write-Host "⚠ Flutter environment has issues!" -ForegroundColor Red
    Write-Host ""
    Write-Host "To fix common issues:" -ForegroundColor Yellow
    Write-Host "  1. Run: flutter doctor --android-licenses" -ForegroundColor White
    Write-Host "  2. Accept all licenses by typing 'y'" -ForegroundColor White
    Write-Host "  3. Install Android SDK if missing" -ForegroundColor White
    Write-Host "  4. Install Java JDK 11 or higher" -ForegroundColor White
    Write-Host ""
    Write-Host "Run this script again after fixing issues." -ForegroundColor Gray
    Write-Host ""
    pause
    exit 1
}

Write-Host "✓ Flutter environment looks good!" -ForegroundColor Green
Write-Host ""

# ==========================================
# STEP 3 - CLEAN PROJECT
# ==========================================

Write-Host "[STEP 3/5] Cleaning Project..." -ForegroundColor Yellow
Write-Host ""

Write-Host "Removing old build files..." -ForegroundColor Gray

flutter clean

Remove-Item ".dart_tool" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "build" -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "✓ Project cleaned successfully" -ForegroundColor Green
Write-Host ""

# ==========================================
# STEP 4 - GET DEPENDENCIES
# ==========================================

Write-Host "[STEP 4/5] Getting Dependencies..." -ForegroundColor Yellow
Write-Host ""

Write-Host "Running flutter pub get..." -ForegroundColor Gray
Write-Host ""

flutter pub get

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Failed to get dependencies!" -ForegroundColor Red
    Write-Host "Check the error messages above." -ForegroundColor Gray
    Write-Host ""
    pause
    exit 1
}

Write-Host ""
Write-Host "✓ Dependencies installed successfully" -ForegroundColor Green
Write-Host ""

# ==========================================
# STEP 5 - BUILD RELEASE APK
# ==========================================

Write-Host "[STEP 5/5] Building Release APK..." -ForegroundColor Yellow
Write-Host ""
Write-Host "⏱ This will take 2-5 minutes..." -ForegroundColor Gray
Write-Host "Please wait patiently..." -ForegroundColor Gray
Write-Host ""

$startTime = Get-Date

flutter build apk --release

$endTime = Get-Date
$duration = New-TimeSpan -Start $startTime -End $endTime

Write-Host ""
Write-Host "══════════════════════════════════════════════" -ForegroundColor Cyan

if ($LASTEXITCODE -eq 0) {
    Write-Host "     ✓ APK BUILD SUCCESSFUL!" -ForegroundColor Green
    Write-Host "══════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
    
    $apkPath = "$PROJECT\mobile_app\build\app\outputs\flutter-apk\app-release.apk"
    
    if (Test-Path $apkPath) {
        Write-Host "APK Location:" -ForegroundColor Yellow
        Write-Host $apkPath -ForegroundColor White
        Write-Host ""
        
        $fileSize = (Get-Item $apkPath).Length / 1MB
        Write-Host "File Size: $([math]::Round($fileSize, 2)) MB" -ForegroundColor Gray
        Write-Host ""
        Write-Host "Build Duration: $([math]::Round($duration.TotalMinutes, 2)) minutes" -ForegroundColor Gray
        Write-Host ""
        
        Write-Host "📱 Next Steps:" -ForegroundColor Yellow
        Write-Host "  1. Transfer APK to Android device" -ForegroundColor White
        Write-Host "  2. Enable 'Install from Unknown Sources'" -ForegroundColor White
        Write-Host "  3. Install the APK" -ForegroundColor White
        Write-Host "  4. Open LIFEASY app" -ForegroundColor White
        Write-Host "  5. Login with test credentials:" -ForegroundColor White
        Write-Host "     Tenant ID: 1001" -ForegroundColor Gray
        Write-Host "     Password: 123456" -ForegroundColor Gray
        Write-Host ""
    } else {
        Write-Host "⚠ WARNING: APK file not found at expected location" -ForegroundColor Yellow
        Write-Host "Check build output folder manually." -ForegroundColor Gray
    }
    
} else {
    Write-Host "     ✗ APK BUILD FAILED" -ForegroundColor Red
    Write-Host "══════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Common solutions:" -ForegroundColor Yellow
    Write-Host "  1. Check gradle.properties memory settings" -ForegroundColor White
    Write-Host "  2. Run: flutter doctor --android-licenses" -ForegroundColor White
    Write-Host "  3. Clean and rebuild: flutter clean && flutter pub get" -ForegroundColor White
    Write-Host "  4. Check error messages above for details" -ForegroundColor White
    Write-Host ""
}

Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
