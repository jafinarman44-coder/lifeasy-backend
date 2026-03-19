# 🚀 LIFEASY V30 PRO - QUICK START COMMANDS

## ⚡ ONE-LINE BUILD & RUN

### Complete Build Sequence:
```powershell
cd "E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\mobile_app" ; flutter clean ; flutter pub get ; flutter build apk --release
```

---

## 📱 MOBILE APP COMMANDS

### Build Release APK:
```powershell
cd mobile_app
flutter clean
flutter pub get
flutter build apk --release
```

**Output:** `mobile_app/build/app/outputs/flutter-apk/app-release.apk`

### Build Debug APK (Faster for testing):
```powershell
flutter build apk --debug
```

### Build App Bundle (For Google Play):
```powershell
flutter build appbundle --release
```

**Output:** `mobile_app/build/app/outputs/bundle/release/app-release.aab`

### Install on Connected Device:
```powershell
flutter install
```

### Run in Debug Mode:
```powershell
flutter run
```

---

## 🌐 BACKEND COMMANDS

### Start Backend (Development):
```powershell
cd backend
uvicorn main_prod:app --host 0.0.0.0 --port 8000 --reload
```

### Start Backend (Production):
```powershell
cd backend
uvicorn main_prod:app --host 0.0.0.0 --port $PORT
```

### OR use the quick start script:
```powershell
.\start_backend.ps1
```

### Check API Status:
```bash
curl http://localhost:8000/health
```

### View API Documentation:
```
Open browser: http://localhost:8000/docs
```

---

## 🔧 COMPLETE SETUP (FIRST TIME)

### Run Master Setup Script:
```powershell
cd E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27
.\MASTER_PRODUCTION_SETUP.ps1
```

This will:
1. Install all Python packages
2. Setup Flutter dependencies
3. Initialize database
4. Build Flutter APK
5. Start backend server

---

## 🎯 TESTING FLOW

### 1. Start Backend:
```powershell
cd backend
uvicorn main_prod:app --host 0.0.0.0 --port 8000 --reload
```

### 2. Build Mobile App:
```powershell
cd mobile_app
flutter build apk --release
```

### 3. Install APK on Device:
```powershell
adb install build/app/outputs/flutter-apk/app-release.apk
```

### 4. Test App:
- Open app on device
- Enter phone: +8801712345678
- Request OTP (check backend logs for OTP code)
- Verify OTP
- Navigate dashboard
- Test payment WebView

---

## 📊 USEFUL ENDPOINTS

### Authentication:
```http
POST http://localhost:8000/api/send-otp
POST http://localhost:8000/api/verify-otp
POST http://localhost:8000/api/register
POST http://localhost:8000/api/login
```

### Payment:
```http
POST http://localhost:8000/api/payment/create
POST http://localhost:8000/api/payment/execute
GET http://localhost:8000/api/payment/status/{payment_id}
```

### Notifications:
```http
POST http://localhost:8000/api/notification/send
POST http://localhost:8000/api/notification/broadcast
```

---

## 🐛 DEBUG COMMANDS

### Check Flutter Installation:
```powershell
flutter doctor -v
```

### Check Python Version:
```powershell
python --version
```

### List Installed Packages:
```powershell
pip list
```

### View Backend Logs:
```powershell
# Backend logs are shown in terminal where uvicorn is running
```

### Clear Flutter Cache:
```powershell
flutter precache
flutter clean
flutter pub get
```

---

## 🎊 PRODUCTION DEPLOYMENT

### Deploy to Render.com:

1. **Push to GitHub**
2. **Create Web Service on Render**
3. **Configure:**
   - Build Command: `pip install -r backend/requirements.txt`
   - Start Command: `cd backend && uvicorn main_prod:app --host 0.0.0.0 --port $PORT`

### Environment Variables:
Add these in Render dashboard:
```
DATABASE_URL=postgresql://...
JWT_SECRET=your_secret_key
TWILIO_ACCOUNT_SID=...
TWILIO_AUTH_TOKEN=...
BKASH_APP_KEY=...
BKASH_APP_SECRET=...
FIREBASE_CREDENTIALS_PATH=./firebase_credentials.json
```

---

## 📞 SUPPORT COMMANDS

### Get Help:
```powershell
flutter --help
uvicorn --help
pip --help
```

### View Documentation:
```
Backend API Docs: http://localhost:8000/docs
Flutter Docs: https://flutter.dev/docs
FastAPI Docs: https://fastapi.tiangolo.com
```

---

## 🎯 QUICK REFERENCE

| Task | Command |
|------|---------|
| **Build APK** | `flutter build apk --release` |
| **Start Backend** | `uvicorn main_prod:app --host 0.0.0.0 --port 8000` |
| **Install Dependencies** | `flutter pub get` / `pip install -r requirements.txt` |
| **Clean Build** | `flutter clean` |
| **Run Tests** | `flutter test` |
| **Check Health** | `curl http://localhost:8000/health` |
| **View Logs** | Check terminal output |

---

**Version:** 30.0.0-PRO  
**Last Updated:** 2026-03-20  
**Status:** ✅ Production Ready
