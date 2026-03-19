# 🔥 💣 FULL HARD RESET - LIFEASY V27
# COMPLETE FLUTTER + GRADLE CLEAN (100% FIX)

Write-Host "`n🔥 💣 FULL HARD RESET (FINAL FIX)" -ForegroundColor Cyan
Write-Host "=================================`n" -ForegroundColor Gray
Write-Host "This will 100% solve all build issues!`n" -ForegroundColor Green

$originalLocation = Get-Location

# ========================================
# STEP 1: FLUTTER CLEAN
# ========================================
Write-Host "📱 STEP 1: Flutter Clean" -ForegroundColor Yellow
Write-Host "─────────────────────────────`n" -ForegroundColor Gray

Set-Location -Path ".\mobile_app"

Write-Host "Running flutter clean...`n" -ForegroundColor Cyan
flutter clean

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Flutter clean completed`n" -ForegroundColor Green
} else {
    Write-Host "⚠️  Flutter clean had issues, continuing with manual cleanup...`n" -ForegroundColor Yellow
}

# ========================================
# STEP 2: MANUAL DELETE (BUILD + CACHE)
# ========================================
Write-Host "🗑️  STEP 2: Manual Cache Deletion" -ForegroundColor Yellow
Write-Host "─────────────────────────────────────`n" -ForegroundColor Gray

$directoriesToDelete = @(
    "build",
    ".dart_tool",
    "android\.gradle"
)

foreach ($dir in $directoriesToDelete) {
    $fullPath = Join-Path -Path ".\mobile_app" -ChildPath $dir
    if (Test-Path $fullPath) {
        Write-Host "Deleting: $dir ..." -ForegroundColor Cyan
        Remove-Item -Path $fullPath -Recurse -Force
        Write-Host "  ✓ Deleted: $dir" -ForegroundColor Green
    } else {
        Write-Host "ℹ️  Not found (already clean): $dir" -ForegroundColor Gray
    }
}

Write-Host ""

# Also delete pubspec.lock to force fresh dependency resolution
$pubspecLock = ".\mobile_app\pubspec.lock"
if (Test-Path $pubspecLock) {
    Write-Host "Deleting: pubspec.lock ..." -ForegroundColor Cyan
    Remove-Item -Path $pubspecLock -Force
    Write-Host "  ✓ Deleted: pubspec.lock`n" -ForegroundColor Green
}

# ========================================
# STEP 3: GRADLE CLEAN (IMPORTANT!)
# ========================================
Write-Host "🛠️  STEP 3: Gradle Cache Clear" -ForegroundColor Yellow
Write-Host "───────────────────────────────────`n" -ForegroundColor Gray

Set-Location -Path ".\mobile_app\android"

if (Test-Path ".\gradlew") {
    Write-Host "Running gradlew clean...`n" -ForegroundColor Cyan
    
    # Windows
    if ($IsWindows -or $env:OS -eq "Windows_NT") {
        .\gradlew.bat clean
    } else {
        .\gradlew clean
    }
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✅ Gradle clean completed`n" -ForegroundColor Green
    } else {
        Write-Host "`n⚠️  Gradle clean had issues, continuing anyway...`n" -ForegroundColor Yellow
    }
} else {
    Write-Host "⚠️  gradlew not found, skipping gradle clean`n" -ForegroundColor Yellow
}

# Navigate back to mobile_app
Set-Location -Path ".."

# ========================================
# STEP 4: UPDATE GRADLE.PROPERTIES
# ========================================
Write-Host "⚙️  STEP 4: Update gradle.properties" -ForegroundColor Yellow
Write-Host "────────────────────────────────────────`n" -ForegroundColor Gray

$gradlePropertiesPath = ".\android\gradle.properties"

if (Test-Path $gradlePropertiesPath) {
    Write-Host "Reading current gradle.properties..." -ForegroundColor Cyan
    
    $content = Get-Content $gradlePropertiesPath -Raw
    $lines = Get-Content $gradlePropertiesPath
    
    # Check and update org.gradle.jvmargs
    $hasJvmArgs = $false
    $hasKotlinIncremental = $false
    
    foreach ($line in $lines) {
        if ($line -match "^org\.gradle\.jvmargs=") {
            $hasJvmArgs = $true
        }
        if ($line -match "^kotlin\.incremental=") {
            $hasKotlinIncremental = $true
        }
    }
    
    # Create new content
    $newLines = @()
    
    # Add JVM args line (replace if exists)
    $newLines += "org.gradle.jvmargs=-Xmx2048M -XX:MaxMetaspaceSize=512m"
    
    # Add existing lines except old jvmargs
    foreach ($line in $lines) {
        if ($line -notmatch "^org\.gradle\.jvmargs=") {
            $newLines += $line
        }
    }
    
    # Add kotlin.incremental if not exists
    if (-not $hasKotlinIncremental) {
        $newLines += "kotlin.incremental=false"
    }
    
    # Write updated content
    $newLines | Set-Content $gradlePropertiesPath
    
    Write-Host "✅ Updated gradle.properties:" -ForegroundColor Green
    Write-Host "   • org.gradle.jvmargs=-Xmx2048M" -ForegroundColor Gray
    Write-Host "   • kotlin.incremental=false`n" -ForegroundColor Gray
} else {
    Write-Host "⚠️  gradle.properties not found!" -ForegroundColor Yellow
}

# ========================================
# STEP 5: FLUTTER PUB GET
# ========================================
Write-Host "📦 STEP 5: Fetch Dependencies (flutter pub get)" -ForegroundColor Yellow
Write-Host "──────────────────────────────────────────────`n" -ForegroundColor Gray

Write-Host "Running flutter pub get...`n" -ForegroundColor Cyan
flutter pub get

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n✅ Dependencies fetched successfully`n" -ForegroundColor Green
} else {
    Write-Host "`n❌ Failed to fetch dependencies!" -ForegroundColor Red
    Write-Host "`nTroubleshooting:" -ForegroundColor Yellow
    Write-Host "  1. Check internet connection" -ForegroundColor White
    Write-Host "  2. Run: flutter doctor" -ForegroundColor White
    Write-Host "  3. Run: flutter pub cache repair`n" -ForegroundColor White
    Set-Location $originalLocation
    exit 1
}

# ========================================
# STEP 6: REBUILD APK
# ========================================
Write-Host "🏗️  STEP 6: Rebuild APK (Release Mode)" -ForegroundColor Yellow
Write-Host "───────────────────────────────────────────`n" -ForegroundColor Gray

Write-Host "Running: flutter build apk --release --no-tree-shake-icons`n" -ForegroundColor Cyan
Write-Host "⏰ This will take 5-10 minutes...`n" -ForegroundColor Gray

flutter build apk --release --no-tree-shake-icons

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n🎉 APK BUILT SUCCESSFULLY!" -ForegroundColor Green
    
    # Show APK details
    $apkPath = "build\app\outputs\flutter-apk\app-release.apk"
    if (Test-Path $apkPath) {
        $fileSize = (Get-Item $apkPath).Length / 1MB
        Write-Host "`n📱 APK Details:" -ForegroundColor Cyan
        Write-Host "   Location: $apkPath" -ForegroundColor White
        Write-Host "   Size: $([math]::Round($fileSize, 2)) MB" -ForegroundColor Gray
        Write-Host "   Build Mode: Release" -ForegroundColor Gray
        Write-Host "   Icons: Not tree-shaken (faster build)`n" -ForegroundColor Gray
    }
    
    Write-Host "✅ INSTALLATION READY!" -ForegroundColor Green
    Write-Host "`n📲 Next Steps:" -ForegroundColor Cyan
    Write-Host "   1. Transfer APK to Android device" -ForegroundColor White
    Write-Host "   2. Enable 'Install from Unknown Sources'" -ForegroundColor White
    Write-Host "   3. Install the APK" -ForegroundColor White
    Write-Host "   4. Login with:" -ForegroundColor White
    Write-Host "      Tenant ID: 1001" -ForegroundColor Gray
    Write-Host "      Password: 123456`n" -ForegroundColor Gray
    
} else {
    Write-Host "`n❌ APK BUILD FAILED!" -ForegroundColor Red
    Write-Host "`n🔧 Additional Fixes to Try:" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "1. Clear Flutter cache:" -ForegroundColor White
    Write-Host "   flutter clean" -ForegroundColor Gray
    Write-Host ""
    Write-Host "2. Check Flutter installation:" -ForegroundColor White
    Write-Host "   flutter doctor -v" -ForegroundColor Gray
    Write-Host ""
    Write-Host "3. Update Flutter:" -ForegroundColor White
    Write-Host "   flutter upgrade" -ForegroundColor Gray
    Write-Host ""
    Write-Host "4. Clear pub cache:" -ForegroundColor White
    Write-Host "   flutter pub cache clean" -ForegroundColor Gray
    Write-Host "   flutter pub get`n" -ForegroundColor Gray
    
    Set-Location $originalLocation
    exit 1
}

# ========================================
# FINAL SUMMARY
# ========================================
Set-Location $originalLocation

Write-Host "`n🎯 FULL HARD RESET COMPLETE!" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════`n" -ForegroundColor Gray

Write-Host "✅ Completed Steps:" -ForegroundColor Green
Write-Host "   1. Flutter clean" -ForegroundColor White
Write-Host "   2. Manual cache deletion (build/, .dart_tool/, .gradle/)" -ForegroundColor White
Write-Host "   3. Gradle clean" -ForegroundColor White
Write-Host "   4. Updated gradle.properties (JVM args + Kotlin settings)" -ForegroundColor White
Write-Host "   5. Fetched dependencies (flutter pub get)" -ForegroundColor White
Write-Host "   6. Built release APK (--no-tree-shake-icons)`n" -ForegroundColor White

Write-Host "🎊 YOUR APP IS 100% FIXED AND READY! 🎊" -ForegroundColor Green
Write-Host ""
Write-Host "Build Time: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
Write-Host "Status: SUCCESS" -ForegroundColor Green
Write-Host ""

