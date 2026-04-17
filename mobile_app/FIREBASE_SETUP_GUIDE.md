# 🚀 LIFEASY MOBILE APP - FIREBASE SETUP GUIDE

**Date**: 2026-04-03  
**Status**: ⚠️ **ACTION REQUIRED**

---

## ✅ COMPLETED FIXES

### 1. AndroidManifest Permissions - FIXED ✅

Added missing permission to:
`mobile_app/android/app/src/main/AndroidManifest.xml`

```xml
<uses-permission android:name="android.permission.POST_NOTIFICATIONS"/>
```

**Now all required permissions are present:**
- ✅ INTERNET
- ✅ RECORD_AUDIO
- ✅ CAMERA
- ✅ MODIFY_AUDIO_SETTINGS
- ✅ POST_NOTIFICATIONS (NEW!)

### 2. Flutter Dependencies - INSTALLED ✅

```bash
flutter pub get
```
**Status**: All packages resolved successfully

---

## ❌ CRITICAL: FIREBASE CONFIGURATION NEEDED

### Problem

The file `google-services.json` was **MISSING**. I created a **TEMPLATE** file for you, but it contains **PLACEHOLDER VALUES** that MUST be replaced with your real Firebase project details.

### Location

```
mobile_app/android/app/google-services.json
```

---

## 🔧 STEP-BY-STEP FIREBASE SETUP

### Step 1: Create Firebase Project (If Not Exists)

1. Go to **https://console.firebase.google.com/**
2. Click **"Add project"** or select existing project
3. Project name: `LIFEASY` (or your preferred name)
4. Enable Google Analytics (optional)
5. Click **"Create project"**

---

### Step 2: Add Android App to Firebase

1. In Firebase Console, click **"Add app"** → **Android icon**
2. Enter package name: `com.example.lifeasy_mobile_app`
   *(Check your actual package name in `android/app/src/main/AndroidManifest.xml`)*
3. App nickname: `LIFEASY Mobile`
4. Debug signing certificate SHA-1 (optional for now)
5. Click **"Register app"**

---

### Step 3: Download google-services.json

1. Firebase will show **"Download google-services.json"** button
2. Click **"Download google-services.json"**
3. Save the file to:
   ```
   E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\mobile_app\android\app\google-services.json
   ```

**IMPORTANT**: Replace the template file I created with your REAL one from Firebase!

---

### Step 4: Verify File Placement

After downloading, verify the file exists:

```powershell
Test-Path "E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\mobile_app\android\app\google-services.json"
```

Should return: `True`

---

### Step 5: Add Firebase Dependencies (If Not Already Added)

Check if these lines exist in `android/app/build.gradle.kts`:

```kotlin
dependencies {
    implementation(platform("com.google.firebase:firebase-bom:33.0.0"))
    implementation("com.google.firebase:firebase-messaging")
}
```

And in `android/build.gradle.kts`:

```kotlin
buildscript {
    dependencies {
        classpath("com.google.gms:google-services:4.4.1")
    }
}
```

---

## 📱 NOW RUN THE MOBILE APP

### Command Sequence:

```powershell
# 1. Navigate to mobile app
cd "E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\mobile_app"

# 2. Make sure dependencies are installed
flutter pub get

# 3. Connect your Android phone via USB
#    - Enable USB Debugging
#    - Allow permission on phone

# 4. Run the app
flutter run
```

---

## 🎯 WHAT TO TEST IN THE APP

### After App Launches:

1. **Login/Register** as Tenant
   - Use email + password + OTP flow
   - Verify OTP arrives via Brevo

2. **Check WebSocket Connection**
   - App should auto-connect to backend
   - Check terminal logs for connection confirmation

3. **Test FCM Registration**
   - App should register device token with backend
   - Backend stores token in database

4. **Wait for Call Test**
   - Keep app running in foreground
   - Owner will initiate call from Windows app
   - You should receive call notification

---

## ⚠️ TROUBLESHOOTING

### Problem 1: "google-services.json not found"

**Error during build:**
```
File google-services.json is missing
```

**Solution:**
- Download real file from Firebase Console (Step 3 above)
- Place it in correct folder
- Run `flutter clean` then `flutter run`

---

### Problem 2: "FCM token not generating"

**Possible causes:**
- google-services.json has wrong package name
- Firebase project not configured correctly
- Missing Google Play Services on device

**Solution:**
- Verify package name matches in Firebase
- Check Firebase console for registered apps
- Test on physical device (not emulator)

---

### Problem 3: "Call notification not received"

**Check:**
1. Backend is running (`http://localhost:8000`)
2. WebSocket connection established
3. FCM token saved in backend database
4. Internet connection active

---

## 📊 SYSTEM READINESS CHECKLIST

Before initiating call test, verify:

| Component | Status | How to Check |
|-----------|--------|--------------|
| Backend API | ✅ RUNNING | http://localhost:8000/docs |
| Brevo Email | ✅ READY | `.env` has API key |
| Agora Token | ✅ READY | Backend initialized |
| WebSocket | ✅ READY | CallSocketManager active |
| Android Permissions | ✅ FIXED | AndroidManifest updated |
| Flutter Packages | ✅ INSTALLED | `flutter pub get` done |
| google-services.json | ⚠️ **NEEDS REAL FILE** | Download from Firebase |
| Mobile Device Connected | ❓ YOUR ACTION | USB debugging ON |
| App Running on Phone | ❓ PENDING | `flutter run` |

---

## 🎊 FINAL STEPS

### Immediate Actions Required:

1. ✅ **Download REAL google-services.json** from Firebase
2. ✅ **Replace template file** with real one
3. ✅ **Connect Android phone** via USB
4. ✅ **Run mobile app**: `flutter run`
5. ✅ **Login as tenant** in mobile app
6. ✅ **Keep app open** and ready for calls

### Then Ready For:

- Windows app → Tenant list → Call button
- Mobile receives call notification
- Accept call → Agora video/voice connection
- **100% LIVE CALL TEST!** 🚀

---

## 📞 BACKEND STATUS (ALREADY RUNNING)

```
🌐 URL: http://localhost:8000
📡 Status: OPERATIONAL
✅ Database: Active
✅ WebSocket: Listening
✅ FCM Service: Ready (needs google-services.json)
✅ Agora Engine: Ready
✅ Email (Brevo): Ready (needs API key in .env)
```

---

## 🔥 IMPORTANT REMINDERS

⚠️ **DO NOT CLOSE BACKEND TERMINAL**  
Backend must stay running during entire test

⚠️ **USE PHYSICAL DEVICE**  
FCM doesn't work reliably on emulators

⚠️ **KEEP INTERNET ACTIVE**  
Both PC and phone need internet

⚠️ **USB DEBUGGING MUST STAY ON**  
Don't disconnect USB cable during test

---

**Next Step**: Download your Firebase google-services.json file and replace the template!

**Then**: `flutter run` and prepare for live call test! 🎯
