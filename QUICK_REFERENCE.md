# ⚡ LIFEASY V27 - QUICK REFERENCE CARD

---

## 🎯 ESSENTIAL COMMANDS

### **Backend**
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### **Mobile App**
```powershell
cd mobile_app
flutter pub get
flutter run
# OR
flutter build apk --release
```

---

## 🔑 TEST CREDENTIALS

| Field | Value |
|-------|-------|
| **Tenant ID** | `1001` |
| **Password** | `123456` |
| **OTP** | `123456` |

---

## 🌐 API ENDPOINTS

### Base URL: `http://localhost:8000/api`

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/login` | Tenant login |
| POST | `/send-otp` | Send OTP |
| POST | `/verify-otp` | Verify OTP |
| GET | `/tenants/{id}` | Get profile |
| GET | `/bills/tenant/{id}` | Get bills |
| GET | `/payments/tenant/{id}` | Get payments |

---

## 📱 MOBILE APP STRUCTURE

```
lib/
├── main.dart              (Entry point)
├── services/
│   └── api_service.dart   (API calls)
├── screens/
│   ├── login_screen.dart
│   ├── dashboard_screen.dart
│   ├── bills_screen.dart
│   └── payments_screen.dart
└── widgets/
    └── bill_card.dart
```

---

## 🎨 THEME COLORS

- **Background:** `Color(0xff0f172a)` - Dark blue
- **Accent:** `Colors.blueAccent`
- **Cards:** `Colors.black54`
- **Success:** `Colors.green`
- **Warning:** `Colors.orange`

---

## 📦 KEY PACKAGES

### Backend
- FastAPI
- SQLAlchemy
- Python-Jose (JWT)
- Passlib (bcrypt)
- Uvicorn

### Mobile
- http
- provider
- shared_preferences
- google_fonts

---

## 🔧 CONFIGURATION FILES

| File | Purpose |
|------|---------|
| `backend/main.py` | App entry |
| `backend/auth.py` | JWT tokens |
| `backend/database.py` | DB config |
| `mobile_app/lib/services/api_service.dart` | API URL |

---

## 🚀 BUILD APK STEPS

```powershell
cd mobile_app
flutter clean
flutter pub get
flutter build apk --release
```

**Output:** `build/app/outputs/flutter-apk/app-release.apk`

---

## 🌍 NETWORK SETUP

### Find PC IP:
```powershell
ipconfig
```

### Update in `api_service.dart`:
```dart
static const String baseUrl = 'http://192.168.0.181:8000';
```

### Add Firewall Rule (Admin):
```powershell
netsh advfirewall firewall add rule name="FastAPI8000" dir=in action=allow protocol=TCP localport=8000
```

---

## ✅ VERIFICATION CHECKLIST

- [ ] Backend starts without errors
- [ ] Swagger UI opens at `/docs`
- [ ] Login endpoint works
- [ ] Mobile app connects to backend
- [ ] Login screen displays
- [ ] Dashboard loads after login
- [ ] Bills screen shows data
- [ ] Payments screen shows data
- [ ] APK builds successfully

---

## 🐛 COMMON ISSUES

| Issue | Solution |
|-------|----------|
| Connection refused | Check IP, firewall, backend running |
| Module not found | Run `flutter pub get` |
| Port in use | Change port or stop other service |
| APK not installing | Enable unknown sources |

---

## 📊 PROJECT STATS

- **Backend Files:** 8
- **Mobile Files:** 8
- **Total Lines:** ~1500+
- **API Endpoints:** 10+
- **Screens:** 4
- **Models:** 3
- **Routers:** 4

---

## 🎯 CURRENT FEATURES

✅ JWT Authentication  
✅ Login + OTP System  
✅ Tenant Dashboard  
✅ Bill Management  
✅ Payment History  
✅ Dark Theme UI  
✅ RESTful APIs  
✅ Modular Architecture  
✅ Error Handling  
✅ Loading States  

---

**⚡ You're ready to go!**

All systems operational. Happy coding! 🚀
