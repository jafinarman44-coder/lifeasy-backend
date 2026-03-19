# 📱 LIFEASY V28 - Mobile App Build Guide

## ✅ PRE-BUILD CHECKLIST

### Step 1: Verify Project Structure

Navigate to mobile app folder:
```powershell
cd "E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\mobile_app"
dir
```

**Required folders:**
- ✅ `android/`
- ✅ `ios/`
- ✅ `lib/`

**Required files:**
- ✅ `pubspec.yaml`

---

### Step 2: Check Flutter Environment

```powershell
flutter doctor
```

**Expected output (all should have ✓):**
```
✓ Flutter version
✓ Android toolchain - develop for Android devices
✓ Chrome - develop for the web
✓ Visual Studio - develop for Windows
✓ Android Studio
✓ VS Code
✓ Connected device
```

**If you see issues:**

#### Fix Android Licenses:
```powershell
flutter doctor --android-licenses
```
Type `y` to accept all licenses.

#### Fix Java Issues:
Install JDK 11 or higher from: https://adoptium.net/

---

### Step 3: Gradle Memory Fix (CRITICAL)

**File:** `mobile_app/android/gradle.properties`

**Optimized settings (already applied):**
```properties
org.gradle.jvmargs=-Xmx1024m -XX:MaxMetaspaceSize=512m
android.useAndroidX=true
android.enableJetifier=true
```

⚠️ **IMPORTANT:** This prevents "paging file too small" errors!

---

## 🚀 BUILD PROCESS

### Method 1: Automated Script (Recommended)

```powershell
cd "E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\mobile_app"
.\BUILD_APK_STEP_BY_STEP.ps1
```

This script will:
1. ✅ Verify project structure
2. ✅ Check Flutter environment
3. ✅ Clean old builds
4. ✅ Install dependencies
5. ✅ Build Release APK
6. ✅ Show APK location

**Duration:** 2-5 minutes

---

### Method 2: Manual Commands

```powershell
# Navigate to project
cd "E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\mobile_app"

# Clean project
flutter clean

# Remove old build folders manually
Remove-Item ".dart_tool" -Recurse -Force
Remove-Item "build" -Recurse -Force

# Get dependencies
flutter pub get

# Build release APK
flutter build apk --release
```

---

## 📦 OUTPUT

### Successful Build Location:

```
E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\mobile_app\build\app\outputs\flutter-apk\app-release.apk
```

**Expected file size:** 40-60 MB  
**Build time:** 2-5 minutes

---

## 🧪 TESTING THE APK

### Installation Steps:

1. **Transfer APK to Android device**
   - USB cable
   - Google Drive / Dropbox
   - Email
   - WiFi transfer app

2. **Enable installation:**
   - Settings → Security → Unknown Sources (enable)
   - Or Settings → Apps → Special Access → Install unknown apps

3. **Install:**
   - Open file manager on device
   - Tap `app-release.apk`
   - Follow installation prompts

4. **Test login:**
   ```
   Tenant ID:  1001
   Password:   123456
   OTP:        (Generated on login - check backend console)
   ```

---

## 🔧 TROUBLESHOOTING

### Error: "Gradle build failed"

**Solution 1:** Reduce memory usage
```properties
# Edit android/gradle.properties
org.gradle.jvmargs=-Xmx1024m
```

**Solution 2:** Delete .gradle cache
```powershell
Remove-Item "android/.gradle" -Recurse -Force
flutter clean
flutter pub get
```

---

### Error: "No Android SDK found"

**Solution:**
```powershell
flutter config --android-sdk "C:\Users\YOUR_NAME\AppData\Local\Android\Sdk"
flutter doctor --android-licenses
```

---

### Error: "License agreements not accepted"

**Solution:**
```powershell
flutter doctor --android-licenses
# Type 'y' for each prompt
```

---

### Error: "Java not found" or "JDK missing"

**Solution:**
1. Download JDK 11: https://adoptium.net/
2. Install to default location
3. Set JAVA_HOME environment variable
4. Restart PowerShell
5. Run: `flutter doctor`

---

### Error: "Build failed with exit code 1"

**Common causes:**
- Missing Android SDK
- Unaccepted licenses
- Insufficient Gradle memory
- Corrupted build cache

**Fix:**
```powershell
flutter clean
Remove-Item ".dart_tool" -Recurse -Force
Remove-Item "build" -Recurse -Force
Remove-Item "android/.gradle" -Recurse -Force
flutter pub get
flutter build apk --release
```

---

### Warning: "Paging file too small"

**Already fixed!** The gradle.properties has been updated with:
```properties
org.gradle.jvmargs=-Xmx1024m -XX:MaxMetaspaceSize=512m
```

If issue persists, close other applications to free up RAM.

---

## 📊 BUILD TIME EXPECTATIONS

| Computer Specs | First Build | Subsequent Builds |
|----------------|-------------|-------------------|
| 4GB RAM, HDD   | 5-7 min     | 3-4 min          |
| 8GB RAM, SSD   | 3-5 min     | 2-3 min          |
| 16GB RAM, SSD  | 2-3 min     | 1-2 min          |

**Note:** First build takes longer due to dependency, downloading dependencies.

---

## 🎯 POST-BUILD VERIFICATION

### Check APK was created:

```powershell
$apkPath = "E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\mobile_app\build\app\outputs\flutter-apk\app-release.apk"

if (Test-Path $apkPath) {
    Write-Host "✓ APK found!" -ForegroundColor Green
    Write-Host "Size: $((Get-Item $apkPath).Length / 1MB) MB" -ForegroundColor Gray
} else {
    Write-Host "✗ APK not found!" -ForegroundColor Red
}
```

---

## 🔄 REBUILD COMMANDS

### Quick rebuild (no changes to dependencies):
```powershell
flutter build apk --release
```

### Full clean rebuild:
```powershell
flutter clean
flutter pub get
flutter build apk --release
```

### Debug build (faster, for testing):
```powershell
flutter build apk
```

---

## 📱 CONNECTING TO BACKEND

After installing APK on mobile device:

### Ensure connectivity:

1. **Same WiFi network** as PC
2. **Firewall allows port 8000**
3. **Backend server running** at `http://192.168.0.119:8000`

### Test connection from mobile browser:

```
http://192.168.0.119:8000/health
```

Should return:
```json
{"status":"healthy","database":"connected","system":"operational"}
```

---

## 🎯 SUCCESS CRITERIA

Your build is successful when:

- ✅ `flutter build apk --release` completes without errors
- ✅ APK file exists in `build/app/outputs/flutter-apk/`
- ✅ File size is 40-60 MB
- ✅ APK installs on Android device
- ✅ App opens successfully
- ✅ Can connect to backend API
- ✅ Login works with test credentials

---

## 📞 QUICK REFERENCE

### All commands in one place:

```powershell
# 1. Navigate to project
cd "E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\mobile_app"

# 2. Check Flutter
flutter doctor

# 3. Accept licenses (if needed)
flutter doctor --android-licenses

# 4. Clean project
flutter clean

# 5. Get dependencies
flutter pub get

# 6. Build APK
flutter build apk --release

# 7. Verify APK
ls build\app\outputs\flutter-apk\
```

---

## 🚀 AUTOMATED SCRIPT

For easiest build, use the automated script:

```powershell
cd "E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\mobile_app"
.\BUILD_APK_STEP_BY_STEP.ps1
```

This handles everything automatically! ✅

---

**📱 LIFEASY V28 Mobile App - Built with Flutter**  
*Version 1.0.0 | Production Ready*
