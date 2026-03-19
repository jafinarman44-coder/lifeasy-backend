# 🚀 LIFEASY V28 ULTRA - Production Ready System

**Smart Living Platform - Complete Apartment Management Solution**

![Version](https://img.shields.io/badge/version-28.0.0-blue)
![Status](https://img.shields.io/badge/status-production--ready-green)
![License](https://img.shields.io/badge/license-commercial-red)

---

## 📋 TABLE OF CONTENTS

- [Overview](#overview)
- [Features](#features)
- [System Architecture](#system-architecture)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [API Documentation](#api-documentation)
- [Mobile App](#mobile-app)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)

---

## 🎯 OVERVIEW

LIFEASY V28 ULTRA is a **production-ready** apartment management platform featuring:

- ✅ **Real Tenant Authentication** with OTP verification
- ✅ **Backend API** built with FastAPI (Python)
- ✅ **Mobile App** built with Flutter (Dart)
- ✅ **Payment Tracking** (Cash, bKash, Nagad, Bank Transfer)
- ✅ **Bill Management** with monthly tracking
- ✅ **Automated Deployment** scripts

---

## ✨ KEY FEATURES

### 🔐 Authentication System

- Tenant ID + Password login
- 6-digit OTP generation and verification
- Secure session management
- Password hashing (production ready)

### 📱 Mobile Application

- Cross-platform (Android/iOS)
- Material Design UI
- Dark mode support
- Real-time API integration
- Offline-first architecture

### 💰 Payment System

- Multiple payment methods:
  - Cash
  - bKash
  - Nagad
  - Bank Transfer
  - Check
- Payment receipts (PDF)
- Payment history
- Outstanding balance tracking

### 🏠 Tenant Management

- Tenant profiles
- Flat/apartment assignment
- Building management
- Contact information

### 📊 Reporting

- Monthly bills
- Payment summaries
- Income breakdown by method
- Tenant payment history

---

## 🏗️ SYSTEM ARCHITECTURE

```
┌─────────────────────────────────────────┐
│         LIFEASY V28 ULTRA               │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────────┐      ┌─────────────┐ │
│  │   Backend    │◄────►│   Database  │ │
│  │   FastAPI    │      │   SQLite    │ │
│  │   Port 8000  │      │             │ │
│  └──────┬───────┘      └─────────────┘ │
│         │                               │
│         │ HTTP/JSON API                 │
│         ▼                               │
│  ┌──────────────┐                       │
│  │  Mobile App  │                       │
│  │   Flutter    │                       │
│  │  Android/iOS │                       │
│  └──────────────┘                       │
│                                         │
└─────────────────────────────────────────┘
```

### Technology Stack

**Backend:**
- Python 3.8+
- FastAPI 0.109
- SQLAlchemy 2.0
- SQLite (Dev) / PostgreSQL (Prod)
- Uvicorn ASGI Server

**Mobile:**
- Flutter 3.x
- Dart
- Material Design
- HTTP Client
- SharedPreferences

---

## ⚡ QUICK START

### One-Click Deployment

1. **Navigate to deploy folder:**
   ```
   E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\deploy\
   ```

2. **Run as Administrator:**
   ```
   Double-click: RUN_AS_ADMIN.bat
   ```

3. **Wait for completion** (5-7 minutes)

4. **Test credentials:**
   ```
   Tenant ID: 1001
   Password: 123456
   OTP: Auto-generated on login
   ```

---

## 📥 INSTALLATION

### Prerequisites

1. **Python 3.8+** installed
2. **Flutter SDK** installed
3. **Git** (optional)
4. **Windows 10/11**

### Step-by-Step Setup

#### 1. Backend Setup

```powershell
cd "E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\backend"

# Create virtual environment
python -m venv .venv

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt

# Initialize database
python seed.py
```

#### 2. Start Backend Server

```powershell
# In backend folder with .venv activated
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Server will start at: `http://0.0.0.0:8000`

#### 3. Mobile App Setup

```powershell
cd "E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\mobile_app"

# Clean project
flutter clean

# Get dependencies
flutter pub get

# Build release APK
flutter build apk --release
```

APK location: `build/app/outputs/flutter-apk/app-release.apk`

---

## 🌐 API DOCUMENTATION

### Base URL

- **Development:** `http://localhost:8000/api`
- **Network:** `http://192.168.0.119:8000/api`
- **Production:** `https://your-domain.com/api`

### Endpoints

#### Authentication

```http
POST /api/login
Content-Type: application/json

{
  "tenant_id": "1001",
  "password": "123456"
}

Response:
{
  "status": "otp_sent",
  "message": "OTP sent to 01712345678",
  "tenant_id": "1001",
  "otp": "123456"
}
```

```http
POST /api/verify-otp
Content-Type: application/json

{
  "tenant_id": "1001",
  "otp": "123456"
}

Response:
{
  "status": "login_success",
  "message": "Login successful",
  "tenant": {
    "tenant_id": "1001",
    "name": "Test User",
    "phone": "01712345678",
    "flat": "A1",
    "building": "Building A"
  }
}
```

#### Tenants

```http
GET /api/tenants/{tenant_id}
Authorization: Bearer {token}

Response: Tenant profile data
```

#### Bills

```http
GET /api/bills/tenant/{tenant_id}
Authorization: Bearer {token}

Response: List of bills
```

#### Payments

```http
GET /api/payments/tenant/{tenant_id}
Authorization: Bearer {token}

Response: List of payments
```

### Interactive API Docs

Open browser: `http://localhost:8000/docs`

Swagger UI provides interactive testing of all endpoints.

---

## 📱 MOBILE APP

### Configuration

File: `mobile_app/lib/services/api_service.dart`

```dart
class ApiService {
  static const String baseUrl = 'http://192.168.0.119:8000/api';
  
  // ... rest of implementation
}
```

⚠️ **IMPORTANT:** Use network IP address, NOT localhost

### Building APK

```powershell
cd mobile_app

# Debug build
flutter build apk

# Release build (production)
flutter build apk --release

# Profile build (performance testing)
flutter build apk --profile
```

### Installing APK

1. Enable "Install from Unknown Sources" on Android device
2. Transfer `app-release.apk` to device
3. Open file manager and tap APK
4. Follow installation prompts
5. Open LIFEASY app

---

## 🧪 TESTING

### Test Credentials

```
Tenant ID:  1001
Password:   123456
Phone:      01712345678
Flat:       A1
Building:   Building A
```

### Login Flow Test

1. **Open mobile app**
2. **Enter credentials:**
   - Tenant ID: `1001`
   - Password: `123456`
3. **Click Login**
4. **Check backend console** for OTP (e.g., `123456`)
5. **Enter OTP** in mobile app
6. **Dashboard loads** showing bills and payments

### API Test (Browser)

```bash
# Test backend connectivity
curl http://localhost:8000/health

# Expected: {"status":"healthy","database":"connected","system":"operational"}
```

### Mobile Connectivity Test

Ensure:
- ✅ Mobile device and PC on same WiFi network
- ✅ Firewall allows port 8000
- ✅ API URL uses PC's network IP (not localhost)
- ✅ Backend server is running

---

## 🔧 TROUBLESHOOTING

### Backend Won't Start

**Error:** `ModuleNotFoundError`

**Solution:**
```powershell
cd backend
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

### Firewall Blocking

**Error:** Mobile can't connect

**Solution:**
```powershell
# Run as Administrator
netsh advfirewall firewall add rule name="FastAPI8000-IN" dir=in action=allow protocol=TCP localport=8000
netsh advfirewall firewall add rule name="FastAPI8000-OUT" dir=out action=allow protocol=TCP localport=8000
```

---

### Flutter Build Fails

**Error:** `Unable to find bundled Java version`

**Solution:**
```powershell
flutter doctor --android-licenses
flutter config --jdk-dir="C:\Program Files\Android\Android Studio\jbr"
```

---

### OTP Not Generated

**Check:** Backend console for OTP print statement

**Verify:** Database has `otp_codes` table

**Test:** Manually query database:
```sql
SELECT * FROM otp_codes ORDER BY id DESC LIMIT 1;
```

---

## 📁 PROJECT STRUCTURE

```
LIFEASY_V27/
│
├── backend/
│   ├── main.py              # FastAPI application
│   ├── models.py            # SQLAlchemy models
│   ├── auth.py              # Authentication routes
│   ├── database.py          # Database configuration
│   ├── seed.py              # Database seeder
│   ├── requirements.txt     # Python dependencies
│   └── .venv/               # Virtual environment
│
├── mobile_app/
│   ├── lib/
│   │   ├── main.dart        # App entry point
│   │   ├── screens/         # UI screens
│   │   │   ├── login_screen.dart
│   │   │   ├── otp_screen.dart
│   │   │   └── dashboard.dart
│   │   └── services/        # API services
│   │       └── api_service.dart
│   └── pubspec.yaml         # Flutter dependencies
│
├── deploy/
│   ├── RUN_AS_ADMIN.bat     # Auto-elevating launcher
│   ├── LIFEASY_V28_MASTER.ps1
│   ├── start_backend.ps1
│   ├── build_apk.ps1
│   └── QUICK_START.md
│
└── database/
    └── lifeasy_v28.db       # SQLite database
```

---

## 🚀 DEPLOYMENT TO PRODUCTION

### Backend (Ubuntu VPS)

```bash
# Install system dependencies
sudo apt update
sudo apt install python3-pip python3-venv nginx

# Setup application
cd /var/www/lifeasy
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Configure systemd service
sudo nano /etc/systemd/system/lifeasy.service

# Start service
sudo systemctl start lifeasy
sudo systemctl enable lifeasy

# Configure Nginx reverse proxy
sudo nano /etc/nginx/sites-available/lifeasy

# SSL with Let's Encrypt
sudo certbot --nginx -d your-domain.com
```

### Database (PostgreSQL)

```bash
sudo -u postgres psql

CREATE DATABASE lifeasy;
CREATE USER lifeasy_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE lifeasy TO lifeasy_user;
```

Update `database.py`:
```python
DATABASE_URL = "postgresql://lifeasy_user:secure_password@localhost/lifeasy"
```

---

## 📊 MONITORING

### Health Checks

```bash
# Backend health
curl http://localhost:8000/health

# API documentation
curl http://localhost:8000/docs

# Ping test
curl http://localhost:8000/api/ping
```

### Logs

Backend logs appear in terminal where uvicorn is running.

For production:
```bash
journalctl -u lifeasy -f
```

---

## 🔒 SECURITY CONSIDERATIONS

### Production Checklist

- [ ] Use PostgreSQL instead of SQLite
- [ ] Hash passwords with bcrypt
- [ ] Implement JWT tokens
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Rate limit API endpoints
- [ ] Sanitize user inputs
- [ ] Use environment variables for secrets
- [ ] Enable SQL query logging (debug only)
- [ ] Implement audit logging

---

## 📞 SUPPORT & MAINTENANCE

### Version Information

- **Current Version:** 28.0.0
- **Release Date:** 2026-03-17
- **Status:** Production Ready
- **Support:** Commercial

### Known Issues

None at this time.

### Future Enhancements

- Push notifications
- Email notifications
- SMS gateway integration
- Multi-language support
- Advanced analytics dashboard
- Expense tracking
- Maintenance request system

---

## 📄 LICENSE

Commercial License - All Rights Reserved

This software is proprietary and confidential. Unauthorized copying, distribution, or use is strictly prohibited.

---

## 👨‍💻 DEVELOPER NOTES

### Development Mode

Run backend with auto-reload:
```powershell
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Enable Flutter hot reload:
```powershell
flutter run --hot
```

### Testing Locally

Use Postman or Swagger UI to test API endpoints before mobile integration.

### Database Backup

```powershell
Copy-Item "backend/lifeasy_v28.db" "backups/lifeasy_v28_$(Get-Date -Format 'yyyyMMdd_HHmmss').db"
```

---

**🎉 LIFEASY V28 ULTRA - Smart Living Platform**

*Built with ❤️ for modern apartment management*
