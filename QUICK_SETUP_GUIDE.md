# 🚀 LIFEASY V28 ULTRA - QUICK SETUP GUIDE

## ✅ ALL STAGES IN ONE PLACE

---

## 🔥 ONE-CLICK COMPLETE SETUP

### **Automated Script (Recommended)**

```powershell
cd "E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27"
.\COMPLETE_SETUP_ALL_STAGES.ps1
```

**This will automatically:**
- ✅ Initialize database with test tenant
- ✅ Start backend server
- ✅ Clean mobile project
- ✅ Fix Gradle memory
- ✅ Build Release APK
- ✅ Show APK location & credentials

**Duration:** 5-10 minutes

---

## 📋 MANUAL STEP-BY-STEP

### **STAGE 1 - Backend Setup**

```powershell
# Navigate to backend
cd "E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\backend"

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Initialize database
python seed.py

# Start backend server
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**Test:** Open browser → `http://localhost:8000/docs`

✅ **Success:** Swagger UI opens

---

### **STAGE 2 - Mobile Project Clean**

```powershell
# Navigate to mobile app
cd "E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\mobile_app"

# Clean project
flutter clean

# Remove cache manually
Remove-Item ".dart_tool" -Recurse -Force
Remove-Item "build" -Recurse -Force
```

✅ **Success:** Old builds removed

---

### **STAGE 3 - Gradle Memory Fix**

**File:** `mobile_app/android/gradle.properties`

**Content:**
```properties
org.gradle.jvmargs=-Xmx1024m -XX:MaxMetaspaceSize=512m
android.useAndroidX=true
android.enableJetifier=true
```

✅ **Prevents:** "Paging file too small" error

---

### **STAGE 4 - APK Build**

```powershell
# Get dependencies
flutter pub get

# Build release APK
flutter build apk --release
```

**Duration:** 3-6 minutes

**Output:**
```
E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\mobile_app\build\app\outputs\flutter-apk\app-release.apk
```

✅ **Success:** APK file created (40-60 MB)

---

## 📱 TEST LOGIN

**Credentials:**
```
Tenant ID:  1001
Password:   123456
OTP Code:   (Auto-generated, check backend console)
```

**Login Flow:**
1. Open mobile app
2. Enter Tenant ID: `1001`
3. Enter Password: `123456`
4. Click "Login"
5. Check backend terminal for OTP (e.g., `OTP for Test User: 123456`)
6. Enter OTP in mobile app
7. Dashboard loads ✅

---

## 🌐 API CONFIGURATION

### **Mobile App URL**

**File:** `mobile_app/lib/services/api_service.dart`

```dart
class ApiService {
  static const String baseUrl = 'http://192.168.0.119:8000/api';
  // ... rest of code
}
```

⚠️ **CRITICAL:** Use network IP (`192.168.0.119`), NOT localhost!

### **Backend URLs**

- **Local:** `http://localhost:8000`
- **Network (Mobile):** `http://192.168.0.119:8000`
- **API Docs:** `http://localhost:8000/docs`
- **Health Check:** `http://localhost:8000/health`

---

## ✅ VERIFICATION CHECKLIST

After setup completes:

- [ ] Backend server running (check terminal)
- [ ] Database initialized (`lifeasy_v28.db` exists)
- [ ] Test tenant created (ID: 1001)
- [ ] Backend accessible at `http://localhost:8000/docs`
- [ ] APK built successfully
- [ ] APK size: 40-60 MB
- [ ] Mobile app configured with network IP
- [ ] Same WiFi network for testing

---

## 🔧 TROUBLESHOOTING

### Backend won't start

```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python seed.py
```

---

### Flutter build fails

```powershell
flutter doctor --android-licenses
# Accept all licenses by typing 'y'

flutter clean
flutter pub get
flutter build apk --release
```

---

### Gradle memory error

Already fixed! File updated:
```
mobile_app/android/gradle.properties
```

Memory set to: `1024MB` (was `8GB`)

---

### Mobile can't connect

1. Ensure same WiFi network
2. Check firewall allows port 8000
3. Verify backend is running
4. Use network IP (not localhost)

**Test from mobile browser:**
```
http://192.168.0.119:8000/health
```

Should return:
```json
{"status":"healthy","database":"connected","system":"operational"}
```

---

## 📦 APK INSTALLATION

### Transfer to Android Device:

1. **USB Cable:**
   - Connect phone to PC
   - Copy APK to phone
   - Install via file manager

2. **Cloud Storage:**
   - Upload to Google Drive
   - Download on phone
   - Install

3. **Email:**
   - Send to yourself
   - Download attachment
   - Install

### Installation Steps:

1. Enable "Install from Unknown Sources"
   - Settings → Security → Unknown Sources (enable)
   
2. Open file manager
3. Tap APK file
4. Follow installation prompts
5. Open LIFEASY app

---

## 🎯 EXPECTED TIMELINE

| Stage | Duration |
|-------|----------|
| Backend Setup | 30 seconds |
| Database Seed | 5 seconds |
| Mobile Clean | 30 seconds |
| Dependencies | 1-2 minutes |
| APK Build | 3-6 minutes |
| **TOTAL** | **5-10 minutes** |

---

## 📞 QUICK COMMANDS

### Full Setup (Automated):
```powershell
cd "E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27"
.\COMPLETE_SETUP_ALL_STAGES.ps1
```

### Backend Only:
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python seed.py
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### Mobile Build Only:
```powershell
cd mobile_app
flutter clean
flutter pub get
flutter build apk --release
```

---

## 🎉 SUCCESS INDICATORS

✅ Backend starts without errors  
✅ Swagger docs open at `http://localhost:8000/docs`  
✅ Database file created (`lifeasy_v28.db`)  
✅ Flutter build completes  
✅ APK file exists in output folder  
✅ APK installs on device  
✅ Login works with test credentials  

---

## 📖 ADDITIONAL RESOURCES

- **Complete Documentation:** `README.md`
- **Build Guide:** `mobile_app/BUILD_GUIDE.md`
- **Setup Summary:** `SETUP_COMPLETE.md`
- **Quick Start:** `deploy/QUICK_START.md`

---

**🏢 LIFEASY V28 ULTRA - Smart Living Platform**  
*Version 28.0.0 | Production Ready*

**Last Updated:** 2026-03-17
