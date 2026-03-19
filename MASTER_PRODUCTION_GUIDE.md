# 🔥 LIFEASY V30 PRO - MASTER PRODUCTION DEPLOYMENT GUIDE

## 📋 TABLE OF CONTENTS

1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Prerequisites](#prerequisites)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Payment Gateway Setup](#payment-gateway-setup)
7. [SMS/OTP Setup](#smsotp-setup)
8. [Firebase Setup](#firebase-setup)
9. [Deployment](#deployment)
10. [API Documentation](#api-documentation)
11. [Troubleshooting](#troubleshooting)

---

## 🎯 OVERVIEW

**LIFEASY V30 PRO** is a production-ready apartment management system with:

- ✅ **Real Phone Authentication** (Twilio/SSL Wireless SMS)
- ✅ **JWT Token Security**
- ✅ **bKash & Nagad Payment Gateway**
- ✅ **Firebase Push Notifications**
- ✅ **PostgreSQL Database**
- ✅ **FastAPI Backend** (Render-ready)
- ✅ **Flutter Mobile App**

---

## 🏗️ ARCHITECTURE

```
┌─────────────────┐
│  Mobile App     │
│  (Flutter)      │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  FastAPI Server │
│  (Render/Cloud) │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│  PostgreSQL DB  │
│  (Production)   │
└────────┬────────┘
         │
         ↓
┌─────────────────────────────────┐
│  External Services:             │
│  • Twilio/SSL Wireless (SMS)    │
│  • bKash/Nagad (Payment)        │
│  • Firebase (Notifications)     │
└─────────────────────────────────┘
```

---

## 📦 PREREQUISITES

### Backend Requirements:
- Python 3.10+
- pip package manager
- PostgreSQL database (local or cloud)

### Mobile App Requirements:
- Flutter SDK 3.0+
- Android Studio / VS Code
- Android SDK (for APK build)

### External Services:
- **Twilio Account** (or SSL Wireless for Bangladesh)
- **bKash Merchant Account** (sandbox or production)
- **Nagad Merchant Account** (sandbox or production)
- **Firebase Project** with FCM enabled

---

## 🔧 INSTALLATION

### Step 1: Clone Repository
```bash
cd LIFEASY_V27
```

### Step 2: Install Backend Packages
```bash
cd backend
pip install -r requirements.txt
```

**Manual Installation:**
```bash
pip install fastapi uvicorn sqlalchemy passlib[bcrypt] python-jose requests twilio firebase-admin httpx psycopg2-binary python-dotenv gunicorn
```

### Step 3: Install Flutter Dependencies
```bash
cd ../mobile_app
flutter pub get
```

### Step 4: Build Flutter APK
```bash
flutter clean
flutter pub get
flutter build apk --release
```

**APK Location:**
```
mobile_app/build/app/outputs/flutter-apk/app-release.apk
```

---

## ⚙️ CONFIGURATION

### Environment Variables (.env)

Create `backend/.env` file (copy from `.env.example`):

```env
# Environment
LIFEASY_ENV=production
DEBUG=False

# Security Keys (CHANGE THESE!)
JWT_SECRET=your_super_secret_jwt_key_change_this_in_production_2026

# Database (PostgreSQL)
DATABASE_URL=postgresql://user:password@host:5432/dbname

# Twilio SMS
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890

# SSL Wireless (Bangladesh - Alternative)
SSL_WIRELESS_API_KEY=your_api_key
SSL_WIRELESS_SENDER_ID=LIFEASY

# bKash Payment
BKASH_APP_KEY=your_app_key
BKASH_APP_SECRET=your_app_secret
BKASH_USERNAME=your_username
BKASH_PASSWORD=your_password
BKASH_BASE_URL=https://checkout.sandbox.bka.sh/v1.2.0-beta

# Nagad Payment
NAGAD_MERCHANT_ID=your_merchant_id
NAGAD_API_KEY=your_api_key
NAGAD_BASE_URL=https://api.sandbox.nagad-payment.com

# Firebase
FIREBASE_CREDENTIALS_PATH=./firebase_credentials.json
FIREBASE_PROJECT_ID=your_project_id

# Server
HOST=0.0.0.0
PORT=${PORT:-8000}
```

---

## 💳 PAYMENT GATEWAY SETUP

### bKash Integration

#### 1. Sandbox Account
1. Visit: https://developer.bka.sh
2. Create sandbox account
3. Get API credentials:
   - App Key
   - App Secret
   - Username
   - Password

#### 2. Configuration
Update `.env`:
```env
BKASH_BASE_URL=https://checkout.sandbox.bka.sh/v1.2.0-beta
BKASH_APP_KEY=your_sandbox_app_key
BKASH_APP_SECRET=your_sandbox_app_secret
BKASH_USERNAME=your_sandbox_username
BKASH_PASSWORD=your_sandbox_password
```

#### 3. Production
For production, change base URL:
```env
BKASH_BASE_URL=https://checkout.bka.sh/v1.2.0-beta
```

### Nagad Integration

#### 1. Merchant Account
1. Contact Nagad for merchant account
2. Get credentials:
   - Merchant ID
   - API Key

#### 2. Configuration
Update `.env`:
```env
NAGAD_BASE_URL=https://api.sandbox.nagad-payment.com
NAGAD_MERCHANT_ID=your_merchant_id
NAGAD_API_KEY=your_api_key
```

---

## 📱 SMS/OTP SETUP

### Twilio (International)

#### 1. Create Account
1. Visit: https://www.twilio.com
2. Sign up for account
3. Get credentials from dashboard

#### 2. Configuration
Update `.env`:
```env
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=+1234567890
```

### SSL Wireless (Bangladesh)

#### 1. Create Account
1. Visit: https://sslwireless.com
2. Create account
3. Get API key

#### 2. Configuration
Update `.env`:
```env
SSL_WIRELESS_API_KEY=your_api_key
SSL_WIRELESS_SENDER_ID=LIFEASY
```

---

## 🔔 FIREBASE SETUP

### 1. Create Firebase Project
1. Visit: https://console.firebase.google.com
2. Create new project
3. Enable Cloud Messaging (FCM)

### 2. Download Service Account Key
1. Go to Project Settings
2. Service Accounts tab
3. Generate New Private Key
4. Save as `firebase_credentials.json`

### 3. Place Credentials
Copy `firebase_credentials.json` to `backend/` directory

### 4. Update .env
```env
FIREBASE_CREDENTIALS_PATH=./firebase_credentials.json
FIREBASE_PROJECT_ID=your_project_id
```

---

## 🚀 DEPLOYMENT

### Deploy to Render.com

#### 1. Prepare Repository
Push code to GitHub/GitLab

#### 2. Create Web Service on Render
1. Login to https://render.com
2. Create New Web Service
3. Connect repository

#### 3. Configuration
**Build Command:**
```bash
pip install -r backend/requirements.txt
```

**Start Command:**
```bash
cd backend && uvicorn main_prod:app --host 0.0.0.0 --port $PORT
```

#### 4. Environment Variables
Add all `.env` variables in Render dashboard

#### 5. Database
Use Render PostgreSQL or external database

### Deploy to Heroku

#### 1. Create Procfile
```
web: cd backend && uvicorn main_prod:app --host 0.0.0.0 --port $PORT
```

#### 2. Deploy
```bash
heroku create lifeasy-api
git push heroku main
```

### Self-Hosted (VPS/Cloud)

#### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 2. Setup Nginx (Reverse Proxy)
```nginx
server {
    listen 80;
    server_name api.lifeasy.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

#### 3. Start with Systemd
```ini
[Unit]
Description=Lifeasy API
After=network.target

[Service]
User=www-data
WorkingDirectory=/path/to/backend
ExecStart=/usr/bin/uvicorn main_prod:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## 📖 API DOCUMENTATION

### Base URL
```
Development: http://localhost:8000/api
Production: https://your-domain.com/api
```

### Interactive Docs
```
http://localhost:8000/docs
```

### Authentication Endpoints

#### 1. Send OTP
```http
POST /api/send-otp
Content-Type: application/json

{
  "phone": "+8801712345678"
}
```

**Response:**
```json
{
  "message": "OTP sent successfully",
  "phone": "+8801712345678",
  "expires_in": 300
}
```

#### 2. Verify OTP
```http
POST /api/verify-otp
Content-Type: application/json

{
  "phone": "+8801712345678",
  "otp": "123456"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "tenant_id": "TNT17123456",
  "phone": "+8801712345678",
  "expires_in": 2592000
}
```

#### 3. Register
```http
POST /api/register
Content-Type: application/json

{
  "phone": "+8801712345678",
  "password": "securepassword123",
  "name": "John Doe"
}
```

#### 4. Login (Password)
```http
POST /api/login
Content-Type: application/json

{
  "phone": "+8801712345678",
  "password": "securepassword123"
}
```

### Payment Endpoints

#### 1. Create Payment
```http
POST /api/payment/create
Content-Type: application/json

{
  "tenant_id": "TNT17123456",
  "amount": 1000,
  "description": "Rent Payment",
  "payment_method": "bkash"
}
```

**Response:**
```json
{
  "success": true,
  "message": "bKash payment created",
  "payment_url": "https://checkout.sandbox.bka.sh/...",
  "payment_id": "PAY123456",
  "transaction_id": "TXN789012"
}
```

#### 2. Execute Payment
```http
POST /api/payment/execute
Content-Type: application/json

{
  "payment_id": "PAY123456",
  "transaction_id": "TXN789012"
}
```

### Notification Endpoints

#### Send Push Notification
```http
POST /api/notification/send
Content-Type: application/json

{
  "tenant_id": "TNT17123456",
  "title": "Payment Successful",
  "body": "Your payment of ৳1000 has been received",
  "type": "payment"
}
```

---

## 🐛 TROUBLESHOOTING

### Backend Issues

#### Database Connection Error
```bash
# Check DATABASE_URL format
echo $DATABASE_URL

# Test PostgreSQL connection
psql $DATABASE_URL
```

#### Port Already in Use
```bash
# Change port
export PORT=8001
uvicorn main_prod:app --host 0.0.0.0 --port $PORT
```

### Mobile App Issues

#### OTP Not Sending
1. Check Twilio credentials in `.env`
2. Verify phone number format (+880...)
3. Check SMS service balance

#### Payment WebView Not Loading
1. Ensure `webview_flutter` is installed
2. Check internet permission in AndroidManifest.xml
3. Verify payment gateway credentials

#### JWT Token Expired
Tokens expire after 30 days by default. User needs to login again.

To refresh token:
```http
POST /api/refresh-token
Content-Type: application/json

{
  "token": "expired_token_here"
}
```

### Firebase Issues

#### Notifications Not Received
1. Check `firebase_credentials.json` exists
2. Verify device token is saved in database
3. Check Firebase console for delivery status

---

## 📊 MONITORING

### Health Check Endpoint
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "database": "connected",
  "services": {
    "auth": "JWT + OTP",
    "payment": "bKash + Nagad",
    "notification": "Firebase"
  }
}
```

### API Status
```http
GET /api/status
```

---

## 🔒 SECURITY BEST PRACTICES

1. **Change Default Secrets**
   - Update `JWT_SECRET` in production
   - Use strong, random passwords

2. **Environment Variables**
   - Never commit `.env` to Git
   - Use secrets management in production

3. **HTTPS Only**
   - Always use HTTPS in production
   - Configure SSL certificate

4. **CORS Configuration**
   - Specify exact allowed origins
   - Don't use `*` in production

5. **Rate Limiting**
   - Implement rate limiting for OTP endpoints
   - Prevent brute force attacks

---

## 📈 PERFORMANCE OPTIMIZATION

### Database
- Use connection pooling
- Add indexes on frequently queried columns
- Enable query logging for debugging

### API
- Use caching (Redis) for OTP storage
- Enable gzip compression
- Use CDN for static assets

### Mobile App
- Optimize images
- Use lazy loading
- Minimize network calls

---

## 🎉 SUCCESS CHECKLIST

- [ ] Backend packages installed
- [ ] PostgreSQL database configured
- [ ] Environment variables set
- [ ] Twilio SMS working
- [ ] bKash/Nagad payment tested
- [ ] Firebase notifications active
- [ ] Flutter APK built
- [ ] Backend deployed to cloud
- [ ] Mobile app tested end-to-end
- [ ] Monitoring setup

---

## 📞 SUPPORT

For issues or questions:
- Check API docs: `/docs`
- Review logs in backend
- Test endpoints with Postman

---

**🚀 CONGRATULATIONS! YOUR PRODUCTION SYSTEM IS READY!**

**Version:** 30.0.0-PRO  
**Last Updated:** 2026-03-20
