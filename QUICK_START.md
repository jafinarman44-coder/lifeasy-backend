# 🚀 LIFEASY V27 - QUICK START GUIDE

---

## ▶️ START EVERYTHING FROM SCRATCH

### **Step 1: Start Backend** (Terminal 1)

```powershell
cd "E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\backend"
.\.venv\Scripts\Activate.ps1
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

✅ You should see: `Uvicorn running on http://0.0.0.0:8000`

---

### **Step 2: Test Backend** (Browser)

Open in browser:
```
http://localhost:8000
http://localhost:8000/docs
```

✅ Should show: "LIFEASY V27 Backend Running"

---

### **Step 3: Run Mobile App** (Terminal 2)

For development/testing:
```powershell
cd "E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\mobile_app"
flutter run
```

For building APK:
```powershell
flutter clean
flutter pub get
flutter build apk --release
```

---

## 📱 LOGIN TEST

**Mobile App Login Screen:**
- Tenant ID: `1001`
- Password: `123456`
- Click **LOGIN**

✅ Expected: Welcome message appears

---

## 🔧 NETWORK SETUP (For Physical Device)

### Find Your PC IP:
```powershell
ipconfig
```

Look for **IPv4 Address** (e.g., `192.168.0.181`)

### Update Mobile App API URL:

Edit file: `mobile_app/lib/services/api_service.dart`

Change line:
```dart
static const String baseUrl = 'http://192.168.0.181:8000';
```

### Add Firewall Rule (Admin PowerShell):
```powershell
netsh advfirewall firewall add rule name="FastAPI8000" dir=in action=allow protocol=TCP localport=8000
```

---

## 🎯 CURRENT STATUS

✅ **Backend:** RUNNING on port 8000
✅ **Mobile App:** Ready to deploy
✅ **API Service:** Configured
✅ **Login UI:** Working
✅ **Database:** Ready to implement

---

## 📂 IMPORTANT FILES

| File | Purpose |
|------|---------|
| `backend/main.py` | FastAPI server |
| `mobile_app/lib/main.dart` | Flutter app entry |
| `mobile_app/lib/services/api_service.dart` | API integration |
| `mobile_app/android/app/src/main/AndroidManifest.xml` | Android permissions |

---

## ⚡ FAST COMMANDS

**Check backend status:**
```powershell
curl http://localhost:8000
```

**Rebuild mobile app:**
```powershell
cd mobile_app
flutter clean
flutter pub get
flutter build apk --release
```

**Install APK on device:**
```powershell
adb install build/app/outputs/flutter-apk/app-release.apk
```

---

## 🐛 COMMON ISSUES

❌ **"Connection refused"**
- Check if backend is running
- Verify correct IP address
- Ensure firewall allows port 8000

❌ **"Module not found"**
- Run `flutter pub get` in mobile_app folder

❌ **"Port already in use"**
- Stop other services using port 8000
- Or change port in backend command

---

**Happy Coding! 🎉**
