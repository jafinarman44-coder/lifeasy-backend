# 📱 LIFEASY - APK BUILD COMPLETE GUIDE

## ⚠️ CURRENT ISSUE
Flutter SDK at `E:\Flutter\flutter` has path configuration issues and cannot execute.

---

## ✅ SOLUTION: 3 EASY STEPS TO BUILD APK

### STEP 1: Fix Flutter SDK Installation

Open PowerShell and run:

```powershell
# Go to C drive
cd C:\

# Clone fresh Flutter SDK (takes 2-3 minutes)
git clone -b stable https://github.com/flutter/flutter.git

# This will create C:\flutter with proper Flutter installation
```

**Alternative:** Download from https://docs.flutter.dev/get-started/install/windows
- Download Flutter SDK zip
- Extract to: `C:\flutter`

---

### STEP 2: Add Flutter to System PATH

**Method 1: Using PowerShell (Admin)**
```powershell
# Run PowerShell as Administrator
[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\flutter\bin", [EnvironmentVariableTarget]::User)
```

**Method 2: Manual Setup**
1. Press `Windows + R`
2. Type: `sysdm.cpl` → Press Enter
3. Click **Advanced** tab
4. Click **Environment Variables**
5. Under **User variables**, find **Path**
6. Click **Edit**
7. Click **New**
8. Add: `C:\flutter\bin`
9. Click **OK** on all windows

---

### STEP 3: Build APK

**Open NEW PowerShell** (Important: Must be new window!)

```powershell
# Verify Flutter is working
flutter --version

# Navigate to project
cd "e:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\mobile_app"

# Clean old builds
flutter clean

# Get dependencies
flutter pub get

# Build APK (takes 3-5 minutes)
flutter build apk --release
```

---

## 📦 APK OUTPUT LOCATION

After successful build, APK will be at:
```
e:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\mobile_app\build\app\outputs\flutter-apk\app-release.apk
```

---

## 🎯 ONE-CLICK BUILD SCRIPT (After fixing Flutter)

Save this as `QUICK_BUILD.ps1` in mobile_app folder:

```powershell
cd "e:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\mobile_app"
flutter clean
flutter pub get
flutter build apk --release

if (Test-Path "build\app\outputs\flutter-apk\app-release.apk") {
    Write-Host "✅ APK BUILD SUCCESS!" -ForegroundColor Green
    Write-Host "Location: build\app\outputs\flutter-apk\app-release.apk" -ForegroundColor Cyan
} else {
    Write-Host "❌ Build failed. Check errors above." -ForegroundColor Red
}
pause
```

---

## 🔧 ANDROID REQUIREMENTS

### Install Android Studio (if not installed)
1. Download: https://developer.android.com/studio
2. Install Android Studio
3. Open Android Studio
4. Go to: **Settings** → **Android SDK**
5. Install **Android SDK** (API Level 34 recommended)
6. Accept licenses

### Accept Android Licenses
```powershell
flutter doctor --android-licenses
# Type 'y' to accept all
```

---

## 📋 COMPLETE SETUP CHECKLIST

Before building APK, ensure:

- [ ] Flutter SDK installed at `C:\flutter`
- [ ] Flutter added to PATH
- [ ] New PowerShell opened
- [ ] `flutter --version` works
- [ ] Android Studio installed
- [ ] Android SDK installed
- [ ] Android licenses accepted (`flutter doctor --android-licenses`)
- [ ] Run `flutter doctor` - all checks should be ✓

---

## 🚀 QUICK START COMMANDS

### Full Build Sequence (Copy-Paste Ready)
```powershell
# 1. Open new PowerShell
# 2. Navigate to project
cd "e:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\mobile_app"

# 3. Verify Flutter
flutter doctor

# 4. Accept licenses
flutter doctor --android-licenses

# 5. Clean project
flutter clean

# 6. Get packages
flutter pub get

# 7. Build APK
flutter build apk --release

# 8. Check output
dir build\app\outputs\flutter-apk\
```

---

## ❓ TROUBLESHOOTING

### Error: "The system cannot find the path specified"
**Solution:** Flutter SDK path is broken. Reinstall Flutter at `C:\flutter`

### Error: "Android SDK not found"
**Solution:** Install Android Studio and Android SDK

### Error: "License not accepted"
**Solution:** Run `flutter doctor --android-licenses`

### Error: "Gradle build failed"
**Solution:** 
```powershell
flutter clean
flutter pub get
flutter build apk --release
```

---

## 📱 AFTER APK IS BUILT

### Install on Android Device
1. Transfer APK to your Android phone
2. Go to **Settings** → **Security**
3. Enable **"Unknown Sources"** or **"Install unknown apps"**
4. Tap APK file to install
5. Open LIFEASY app

### Test Login
- **Tenant ID:** 1001
- **Password:** 123456

---

## 🎉 SUCCESS INDICATORS

You'll know build succeeded when you see:
```
✓ Built build\app\outputs\flutter-apk\app-release.apk
```

File size should be around **30-50 MB**

---

## 💡 PRO TIPS

1. **Always use NEW PowerShell** after installing Flutter
2. **Run flutter doctor** first to check setup
3. **Clean before rebuild:** `flutter clean`
4. **First build takes longer** (5+ minutes), subsequent builds are faster
5. **Keep Android Studio updated** for latest SDK

---

## 📞 NEED HELP?

If build fails, check:
1. Flutter version: `flutter --version`
2. Doctor status: `flutter doctor -v`
3. License status: `flutter doctor --android-licenses`

Share the error output for specific troubleshooting.

---

**Good luck! 🚀**
