# 📧 LIFEASY Email OTP Setup Guide

## ✅ STEP 1 - BACKEND RUNNING WITH PUBLIC IP

Your backend is now running and accessible on your local network!

**Server Status:** ✅ RUNNING  
**URL:** http://192.168.0.181:8000  
**API Docs:** http://192.168.0.181:8000/docs

The `--host 0.0.0.0` flag makes it accessible to all devices on your network.

---

## 🔐 STEP 2 - CONFIGURE GMAIL APP PASSWORD

### Why App Password?
Gmail requires App Passwords for third-party applications when 2-Factor Authentication (2FA) is enabled. Regular passwords won't work.

### Setup Instructions:

1. **Enable 2-Factor Authentication (if not already):**
   - Go to: https://myaccount.google.com/security
   - Enable "2-Step Verification"

2. **Generate App Password:**
   - Go to: https://myaccount.google.com/apppasswords
   - Sign in to your Google account
   - Click "Create app password"
   - Select App: **Mail**
   - Select Device: **Other (Custom name)** → Enter "LIFEASY Backend"
   - Click "Generate"
   - **Copy the 16-character password** (format: xxxx xxxx xxxx xxxx)

3. **Update `.env` file:**
   ```env
   SMTP_EMAIL=your-email@gmail.com
   SMTP_PASSWORD=xxxx xxxx xxxx xxxx
   TEST_RECEIVER_EMAIL=admin@example.com
   SMTP_DEBUG=False
   ```

4. **Restart the backend server** after updating `.env`

---

## 🧪 STEP 3 - TEST SMTP CONNECTION

Run the test script to verify email sending works:

```bash
cd "E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\backend"
python test_email.py
```

### Expected Output:

✅ **SUCCESS:**
```
============================================================
✅ SUCCESS! Email sent successfully!
============================================================

Check your inbox at: your-email@gmail.com

Your OTP email system is ready to use! 🚀
```

❌ **COMMON ERRORS:**

1. **SMTPAuthenticationError:**
   - Gmail App Password is incorrect
   - Solution: Regenerate App Password and update `.env`

2. **SMTPConnectError:**
   - Firewall/ISP blocking port 587
   - Solution: Check Windows Firewall or try mobile hotspot

3. **Connection Timeout:**
   - Network issue or DNS problem
   - Solution: Check internet connection

---

## 📋 STEP 4 - VERIFY NETWORK ACCESS

### Test from another device on same network:

Open browser on phone/tablet and visit:
```
http://192.168.0.181:8000
```

You should see the LIFEASY API welcome page.

### Test API endpoints:

```bash
# From any device on your network:
curl http://192.168.0.181:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected",
  "services": {
    "auth": "JWT + OTP (V1 + V2)",
    "payment": "bKash + Nagad",
    ...
  }
}
```

---

## 🔥 STEP 5 - ENABLE DEBUG MODE (Optional)

For detailed SMTP error logs during development:

Edit `.env`:
```env
SMTP_DEBUG=True
```

This will print detailed SMTP transaction logs to the console when emails are sent.

---

## 🚀 PRODUCTION EMAIL OPTIONS

### Option A: Brevo (Recommended for Production)
✅ Already configured with your API key  
✅ More reliable than SMTP  
✅ Better deliverability  
✅ Free tier: 300 emails/day  

The backend automatically uses Brevo when `BREVO_API_KEY` is set.

### Option B: Gmail SMTP (Development)
✅ Good for testing
✅ Easy setup
❌ Limited to 500 emails/day
❌ Requires App Password

---

## 📱 MOBILE APP CONFIGURATION

Your Flutter app is already configured to connect to the local backend:

**File:** `mobile_app/lib/services/api_service.dart`  
**Base URL:** `http://192.168.0.181:8000/api`

This matches your current PC IP address, so OTP requests will reach your backend.

---

## 🔍 TROUBLESHOOTING

### Issue: Backend not accessible from other devices

**Solution:**
1. Check Windows Firewall allows port 8000
2. Ensure both devices are on same Wi-Fi network
3. Verify IP address hasn't changed: `ipconfig | findstr "IPv4"`

### Issue: Emails not sending

**Check:**
1. App Password is correct (16 characters, no spaces)
2. Internet connection is active
3. Port 587 is not blocked by firewall
4. Try `python test_email.py` first

### Issue: OTP endpoint returns error

**Check:**
1. Backend is running: http://192.168.0.181:8000/health
2. Database initialized successfully
3. Email credentials configured in `.env`

---

## 📊 CURRENT CONFIGURATION SUMMARY

| Component | Status | Details |
|-----------|--------|---------|
| Backend Server | ✅ Running | http://0.0.0.0:8000 |
| Public IP Access | ✅ Enabled | LAN accessible |
| Mobile App | ✅ Configured | Points to 192.168.0.181:8000 |
| Brevo API | ✅ Configured | For production emails |
| Gmail SMTP | ⚠️ Needs Setup | Add App Password to `.env` |
| APK Build | ✅ Ready | app-release.apk (50.4MB) |

---

## 🎯 NEXT STEPS

1. **Configure Gmail App Password** (or use Brevo)
2. **Run `python test_email.py`** to verify
3. **Install APK** on Android device
4. **Test full registration flow** with email OTP
5. **Verify OTP delivery** to your email

---

**Quick Commands:**

```bash
# Start backend (already running)
cd "E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\backend"
python -m uvicorn main_prod:app --host 0.0.0.0 --port 8000

# Test email
python test_email.py

# Check your IP
ipconfig | findstr "IPv4"

# Rebuild APK if needed
cd ..\mobile_app
flutter build apk --release
```

---

**Need Help?**
- Check backend logs in the terminal where uvicorn is running
- Enable SMTP_DEBUG=True for detailed email errors
- Test with small steps: connectivity → SMTP → OTP flow
