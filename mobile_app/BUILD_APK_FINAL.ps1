# LIFEASY V28 - APK Build Script
# This script will build the APK for your Flutter mobile app

$PROJECT = "e:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\mobile_app"

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║       LIFEASY - ANDROID APK BUILD SCRIPT        ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Navigate to mobile app directory
Set-Location $PROJECT

Write-Host "📱 Project Location: $PROJECT" -ForegroundColor Yellow
Write-Host ""

# Check if Flutter is installed
Write-Host "[CHECK 1] Verifying Flutter Installation..." -ForegroundColor Yellow
Write-Host ""

$flutterCmd = Get-Command flutter -ErrorAction SilentlyContinue

if ($null -eq $flutterCmd) {
    Write-Host "❌ ERROR: Flutter is not found in your system PATH!" -ForegroundColor Red
    Write-Host ""
    Write-Host "📋 To install Flutter on Windows:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "  1. Download Flutter SDK from: https://docs.flutter.dev/get-started/install/windows" -ForegroundColor White
    Write-Host "  2. Extract to: C:\src\flutter" -ForegroundColor White
    Write-Host "  3. Add Flutter to PATH:" -ForegroundColor White
    Write-Host "     - Open System Properties > Environment Variables" -ForegroundColor Gray
    Write-Host "     - Edit 'Path' variable" -ForegroundColor Gray
    Write-Host "     - Add: C:\src\flutter\bin" -ForegroundColor Gray
    Write-Host "  4. Restart PowerShell and run this script again" -ForegroundColor White
    Write-Host ""
    Write-Host "🔗 Quick Download Link:" -ForegroundColor Yellow
    Write-Host "https://storage.googleapis.com/flutter_infra_release/releases/stable/windows/flutter_windows_3.24.5-stable.zip" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host "✅ Flutter is installed!" -ForegroundColor Green
Write-Host ""

# Display Flutter version
Write-Host "[CHECK 2] Flutter Version:" -ForegroundColor Yellow
flutter --version
Write-Host ""

# Run Flutter Doctor
Write-Host "[CHECK 3] Running Flutter Doctor..." -ForegroundColor Yellow
Write-Host ""
flutter doctor
Write-Host ""

# Check for Android SDK issues
Write-Host "[CHECK 4] Verifying Android SDK..." -ForegroundColor Yellow
Write-Host ""

$androidSdkPaths = @(
    "$env:LOCALAPPDATA\Android\Sdk",
    "$env:APPDATA\Local\Android\Sdk",
    "C:\Android\Sdk"
)

$androidSdkFound = $false
foreach ($sdkPath in $androidSdkPaths) {
    if (Test-Path $sdkPath) {
        Write-Host "✅ Android SDK found at: $sdkPath" -ForegroundColor Green
        $androidSdkFound = $true
        break
    }
}

if (!$androidSdkFound) {
    Write-Host "⚠️  Android SDK not found!" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "📋 To install Android SDK:" -ForegroundColor Yellow
    Write-Host "  1. Install Android Studio from: https://developer.android.com/studio" -ForegroundColor White
    Write-Host "  2. Open Android Studio" -ForegroundColor White
    Write-Host "  3. Go to Android Studio Settings and navigate to Android SDK" -ForegroundColor White
    Write-Host "  4. Install Android SDK (API Level 34 recommended)" -ForegroundColor White
    Write-Host "  5. Accept licenses" -ForegroundColor White
    Write-Host ""
}

Write-Host ""

# Accept Android licenses
Write-Host "[CHECK 5] Checking Android Licenses..." -ForegroundColor Yellow
Write-Host ""
flutter doctor --android-licenses 2>&1 | Out-Host
Write-Host ""

# Clean project
Write-Host "[BUILD 1/4] Cleaning project..." -ForegroundColor Yellow
flutter clean
Write-Host ""

# Get dependencies
Write-Host "[BUILD 2/4] Getting dependencies..." -ForegroundColor Yellow
flutter pub get
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to get dependencies!" -ForegroundColor Red
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}
Write-Host ""

# Build APK
Write-Host "[BUILD 3/4] Building Release APK..." -ForegroundColor Yellow
Write-Host "⏱  This will take 2-5 minutes. Please wait..." -ForegroundColor Gray
Write-Host ""

$startTime = Get-Date
flutter build apk --release
$endTime = Get-Date
$duration = $endTime - $startTime

Write-Host ""
Write-Host "[BUILD 4/4] Build Complete!" -ForegroundColor Yellow
Write-Host ""

# Check if build was successful
$apkPath = "$PROJECT\build\app\outputs\flutter-apk\app-release.apk"

if (Test-Path $apkPath) {
    Write-Host "════════════════════════════════════════════════════" -ForegroundColor Green
    Write-Host "           ✅ APK BUILD SUCCESSFUL!                " -ForegroundColor Green
    Write-Host "════════════════════════════════════════════════════" -ForegroundColor Green
    Write-Host ""
    Write-Host "📦 APK Location:" -ForegroundColor Cyan
    Write-Host "   $apkPath" -ForegroundColor White
    Write-Host ""
    
    $fileSize = (Get-Item $apkPath).Length / 1MB
    Write-Host "📊 File Size: $([math]::Round($fileSize, 2)) MB" -ForegroundColor Gray
    Write-Host "⏱  Build Time: $([math]::Round($duration.TotalMinutes, 2)) minutes" -ForegroundColor Gray
    Write-Host ""
    Write-Host "📱 Installation Instructions:" -ForegroundColor Yellow
    Write-Host "  1. Enable 'Install from Unknown Sources' on your Android device" -ForegroundColor White
    Write-Host "  2. Transfer the APK to your device" -ForegroundColor White
    Write-Host "  3. Tap the APK file to install" -ForegroundColor White
    Write-Host "  4. Open LIFEASY app" -ForegroundColor White
    Write-Host ""
    Write-Host "🔐 Test Login Credentials:" -ForegroundColor Yellow
    Write-Host "  - Tenant ID: 1001" -ForegroundColor Gray
    Write-Host "  - Password: 123456" -ForegroundColor Gray
    Write-Host ""
} else {
    Write-Host "════════════════════════════════════════════════════" -ForegroundColor Red
    Write-Host "           ❌ APK BUILD FAILED                     " -ForegroundColor Red
    Write-Host "════════════════════════════════════════════════════" -ForegroundColor Red
    Write-Host ""
    Write-Host "🔧 Common Solutions:" -ForegroundColor Yellow
    Write-Host "  1. Run: flutter doctor --android-licenses" -ForegroundColor White
    Write-Host "  2. Accept all licenses" -ForegroundColor White
    Write-Host "  3. Check error messages above for details" -ForegroundColor White
    Write-Host "  4. Ensure Android SDK is properly installed" -ForegroundColor White
    Write-Host ""
}

Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
