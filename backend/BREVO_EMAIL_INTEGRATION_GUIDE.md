# 🟦 BREVO EMAIL INTEGRATION - QUICK GUIDE

## ✅ What Was Changed

### 1. **email_service.py** - Replaced SMTP with Brevo API
- **Before**: Used Gmail SMTP (smtp.gmail.com)
- **After**: Uses Brevo API (api.brevo.com)
- **Benefit**: Works on Render FREE plan, no SMTP configuration needed

### 2. **.env File** - Added Brevo API Key
- **Removed**: SMTP credentials (host, username, password)
- **Added**: `BREVO_API_KEY=your_api_key_here`
- **Benefit**: Simpler configuration, more reliable

### 3. **auth_v2.py** - No changes needed!
- Already compatible with the new email service
- Will automatically use Brevo when backend restarts

---

## 🔧 SETUP STEPS

### Step 1: Get Your Brevo API Key

1. Go to **https://app.brevo.com/**
2. Sign up/Login (FREE plan works perfectly)
3. Click profile icon (top right) → **"SMTP & API"**
4. Click **"Generate New API Key"**
5. Copy the key (starts with `xkeysib-`)

### Step 2: Update .env File

Open: `backend/.env`

Replace this line:
```
BREVO_API_KEY=your_generated_api_key_here
```

With your real key:
```
BREVO_API_KEY=xkeysib-9JHWBIUBWBWB-827huu82hiuh2uih
```

### Step 3: Restart Backend

```powershell
cd "e:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\backend"
uvicorn main_prod:app --reload
```

---

## 🧪 TEST OTP EMAIL

### Option A: Using Test Script (Recommended)

```powershell
# 1. Edit the test file with your email
notepad backend\test_brevo_email.py
# Change: TEST_EMAIL = "youremail@gmail.com"

# 2. Run the test
python backend\test_brevo_email.py
```

### Option B: Using Swagger UI

1. Open: **http://localhost:8000/docs**
2. Find: **POST /api/auth/v2/register-request**
3. Click **"Try it out"**
4. Enter payload:
```json
{
  "email": "youremail@gmail.com",
  "password": "123456",
  "phone": "01700000000",
  "name": "Test User"
}
```
5. Click **"Execute"**
6. Check your email inbox!

---

## 📊 EXPECTATED RESULTS

### ✅ Success Response
```json
{
  "status": "success",
  "message": "OTP sent successfully"
}
```

**Console Output:**
```
📧 Brevo Response: {"id":12345,"message":"OK"}
```

**Email Inbox:** You'll receive an email with subject:
> "Your LIFEASY OTP Code"

### ❌ Common Errors

**Error 1: BREVO_API_KEY missing**
```
❌ ERROR: BREVO_API_KEY missing in .env
```
**Fix**: Add your API key to `.env` file

**Error 2: Invalid API Key**
```
📧 Brevo Response: {"code":"unauthorized","message":"Invalid API key"}
```
**Fix**: Double-check your API key in `.env`

**Error 3: Backend not running**
```
❌ CONNECTION ERROR!
```
**Fix**: Start the backend server first

---

## 🎯 KEY BENEFITS OF BREVO

✅ **FREE Plan**: 300 emails/day (perfect for testing)
✅ **No SMTP**: Pure API-based, works everywhere
✅ **Reliable**: Professional email service
✅ **Fast**: Instant delivery
✅ **Trackable**: See delivery logs in Brevo dashboard
✅ **Render Compatible**: Deploy to cloud without issues

---

## 📝 FILE LOCATIONS

| File | Path | Purpose |
|------|------|---------|
| Email Service | `backend/utils/email_service.py` | Brevo API integration |
| Environment | `backend/.env` | API key storage |
| Auth Router | `backend/routers/auth_v2.py` | Registration flow |
| Test Script | `backend/test_brevo_email.py` | Quick testing |

---

## 🚀 NEXT STEPS

1. ✅ Get Brevo API key
2. ✅ Update `.env` with real key
3. ✅ Restart backend
4. ✅ Test OTP email
5. ✅ Verify email arrives in inbox
6. ✅ Complete registration flow

---

## 📞 SUPPORT

If you face any issues:

1. Check Brevo dashboard for API logs
2. Verify API key is correct (no extra spaces)
3. Ensure backend is using `.env` (restart server)
4. Check spam folder for emails

---

**Last Updated**: 2026-04-03  
**Version**: V27+ Phase 6  
**Status**: ✅ Production Ready
