# ==========================================
# LIFEASY V28 ULTRA - COMPLETE SETUP
# All Stages Automated (1-4)
# ==========================================

$PROJECT = "E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27"

Write-Host ""
Write-Host "╔══════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   LIFEASY V28 ULTRA - COMPLETE SETUP        ║" -ForegroundColor Cyan
Write-Host "║   Backend + Database + Mobile + APK Build   ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# ==========================================
# STAGE 1 - BACKEND SETUP & DATABASE
# ==========================================

Write-Host "[STAGE 1/4] Backend Setup & Database..." -ForegroundColor Yellow
Write-Host ""

Set-Location "$PROJECT\backend"

Write-Host "Activating virtual environment..." -ForegroundColor Gray
.\.venv\Scripts\Activate.ps1

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to activate virtual environment!" -ForegroundColor Red
    pause
    exit 1
}

Write-Host "✓ Virtual environment activated" -ForegroundColor Green
Write-Host ""

Write-Host "Initializing database (seed.py)..." -ForegroundColor Gray
Write-Host ""

python seed.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠ Database seeding had issues, continuing..." -ForegroundColor Yellow
} else {
    Write-Host "✓ Database initialized successfully" -ForegroundColor Green
}

Write-Host ""
Write-Host "Starting backend server in new window..." -ForegroundColor Gray

Start-Process powershell -ArgumentList "-NoExit", "-Command", @"
cd '$PROJECT\backend'; .\.venv\Scripts\Activate.ps1; python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
"@

Write-Host "Waiting for backend to start (5 seconds)..." -ForegroundColor Gray
Start-Sleep -Seconds 5

Write-Host ""
Write-Host "Testing backend accessibility..." -ForegroundColor Gray

try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/docs" -TimeoutSec 3 -UseBasicParsing
    if ($response.StatusCode -eq 200) {
        Write-Host "✓ Backend API is accessible at http://localhost:8000/docs" -ForegroundColor Green
    }
} catch {
    Write-Host "⚠ Backend may still be starting..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "✅ STAGE 1 COMPLETE - Backend Running" -ForegroundColor Green
Write-Host ""

# ==========================================
# STAGE 2 - MOBILE PROJECT CLEANUP
# ==========================================

Write-Host "[STAGE 2/4] Mobile Project Cleanup..." -ForegroundColor Yellow
Write-Host ""

Set-Location "$PROJECT\mobile_app"

Write-Host "Running flutter clean..." -ForegroundColor Gray

flutter clean

Write-Host "Removing build cache..." -ForegroundColor Gray

Remove-Item ".dart_tool" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item "build" -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "✓ Project cleaned successfully" -ForegroundColor Green
Write-Host ""

Write-Host "✅ STAGE 2 COMPLETE - Mobile Project Cleaned" -ForegroundColor Green
Write-Host ""

# ==========================================
# STAGE 3 - GRADLE MEMORY FIX
# ==========================================

Write-Host "[STAGE 3/4] Gradle Memory Configuration..." -ForegroundColor Yellow
Write-Host ""

$gradlePropsPath = "$PROJECT\mobile_app\android\gradle.properties"

if (Test-Path $gradlePropsPath) {
    $content = Get-Content $gradlePropsPath -Raw
    
    # Update memory settings
    $content = $content -replace 'org\.gradle\.jvmargs=.*', 'org.gradle.jvmargs=-Xmx1024m -XX:MaxMetaspaceSize=512m'
    
    Set-Content $gradlePropsPath $content
    
    Write-Host "Updated gradle.properties:" -ForegroundColor Gray
    Get-Content $gradlePropsPath | Select-String "org.gradle.jvmargs" | ForEach-Object {
        Write-Host "  $_" -ForegroundColor White
    }
    
    Write-Host "✓ Gradle memory settings optimized (1024MB)" -ForegroundColor Green
} else {
    Write-Host "⚠ gradle.properties not found!" -ForegroundColor Red
}

Write-Host ""
Write-Host "✅ STAGE 3 COMPLETE - Gradle Configured" -ForegroundColor Green
Write-Host ""

# ==========================================
# STAGE 4 - DEPENDENCIES & APK BUILD
# ==========================================

Write-Host "[STAGE 4/4] Installing Dependencies & Building APK..." -ForegroundColor Yellow
Write-Host ""

Write-Host "Running flutter pub get..." -ForegroundColor Gray

flutter pub get

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to get dependencies!" -ForegroundColor Red
    pause
    exit 1
}

Write-Host "✓ Dependencies installed" -ForegroundColor Green
Write-Host ""

Write-Host "Building Release APK..." -ForegroundColor Yellow
Write-Host "⏱ This will take 3-6 minutes..." -ForegroundColor Gray
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
        Write-Host "📦 APK Location:" -ForegroundColor Yellow
        Write-Host $apkPath -ForegroundColor White
        Write-Host ""
        
        $fileSize = (Get-Item $apkPath).Length / 1MB
        Write-Host "File Size: $([math]::Round($fileSize, 2)) MB" -ForegroundColor Gray
        Write-Host ""
        Write-Host "Build Duration: $([math]::Round($duration.TotalMinutes, 2)) minutes" -ForegroundColor Gray
        Write-Host ""
        
        Write-Host "📱 Next Steps:" -ForegroundColor Yellow
        Write-Host "  1. Transfer APK to Android device" -ForegroundColor White
        Write-Host "  2. Install the APK" -ForegroundColor White
        Write-Host "  3. Open LIFEASY app" -ForegroundColor White
        Write-Host "  4. Login with credentials below" -ForegroundColor White
        Write-Host ""
        
        Write-Host "══════════════════════════════════════════════" -ForegroundColor Cyan
        Write-Host "           TEST CREDENTIALS" -ForegroundColor Yellow
        Write-Host "══════════════════════════════════════════════" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "  Tenant ID:  1001" -ForegroundColor White
        Write-Host "  Password:   123456" -ForegroundColor White
        Write-Host "  OTP Code:   Check backend terminal" -ForegroundColor White
        Write-Host ""
        Write-Host "══════════════════════════════════════════════" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "🌐 API Configuration:" -ForegroundColor Yellow
        Write-Host "  Network URL: http://192.168.0.119:8000/api" -ForegroundColor White
        Write-Host "  ⚠ localhost won't work on mobile!" -ForegroundColor Gray
        Write-Host ""
        
    } else {
        Write-Host "⚠ WARNING: APK file not found!" -ForegroundColor Yellow
    }
    
} else {
    Write-Host "     ✗ APK BUILD FAILED" -ForegroundColor Red
    Write-Host "══════════════════════════════════════════════" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Common solutions:" -ForegroundColor Yellow
    Write-Host "  1. Run: flutter doctor --android-licenses" -ForegroundColor White
    Write-Host "  2. Check error messages above" -ForegroundColor White
    Write-Host "  3. Ensure sufficient disk space" -ForegroundColor White
    Write-Host ""
}

Write-Host "Backend server is running in separate window" -ForegroundColor Green
Write-Host "API Docs: http://localhost:8000/docs" -ForegroundColor Gray
Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
