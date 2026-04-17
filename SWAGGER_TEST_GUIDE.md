# 🧪 SWAGGER UI ENDPOINT TEST GUIDE

## 📍 SWAGGER DOCS URL
**Open in browser:** https://lifeasy-api.onrender.com/docs

---

## ✅ ENDPOINTS TO TEST

### 1️⃣ TENANT APPROVAL

**Endpoint:** `POST /api/tenants/approve/{tenant_id}`

**Test Steps:**
1. Scroll to `tenants` section
2. Click on `POST /api/tenants/approve/{tenant_id}`
3. Click "Try it out"
4. Enter `tenant_id`: `1`
5. Click "Execute"

**Expected Result:**
```json
{
  "status": "success",
  "message": "Tenant Jewel has been approved successfully",
  "data": {
    "id": 1,
    "name": "Jewel",
    "email": "majadar1din@gmail.com",
    "is_active": true,
    "is_verified": true
  }
}
```

**Status Codes:**
- ✅ `200` = Success (endpoint working)
- ❌ `404` = Not deployed yet
- ❌ `500` = Backend bug (check logs)

---

### 2️⃣ OTP SEND

**Endpoint:** `POST /api/otp/send`

**Test Steps:**
1. Scroll to `otp_payment` section
2. Click on `POST /api/otp/send`
3. Click "Try it out"
4. Enter Request body:
   ```json
   {
     "phone": "01717574875"
   }
   ```
5. Click "Execute"

**Expected Result:**
```json
{
  "status": "success",
  "message": "OTP sent successfully",
  "phone": "01717574875",
  "expires_in": 300
}
```

**Status Codes:**
- ✅ `200` or `201` = Success
- ❌ `400` = Bad request (check phone format)
- ❌ `404` = Not deployed
- ❌ `500` = Server error

---

### 3️⃣ OTP VERIFY

**Endpoint:** `POST /api/otp/verify`

**Test Steps:**
1. Click on `POST /api/otp/verify`
2. Click "Try it out"
3. Enter Request body:
   ```json
   {
     "phone": "01717574875",
     "otp": "123456"
   }
   ```
4. Click "Execute"

**Expected Result (if OTP is valid):**
```json
{
  "status": "success",
  "message": "OTP verified successfully",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "tenant_id": "1",
  "phone": "01717574875",
  "name": "Jewel",
  "expires_in": 43200
}
```

**Expected Result (if OTP is invalid):**
```json
{
  "detail": "Invalid OTP"
}
```

**Status Codes:**
- ✅ `200` = Success (endpoint working)
- ❌ `400` = Invalid OTP (normal for test)
- ❌ `404` = Not deployed

---

### 4️⃣ PAYMENTS LIST

**Endpoint:** `GET /api/payments/tenant/{tenant_id}`

**Test Steps:**
1. Click on `GET /api/payments/tenant/{tenant_id}`
2. Click "Try it out"
3. Enter `tenant_id`: `1`
4. (Optional) `skip`: `0`, `limit`: `50`
5. Click "Execute"

**Expected Result:**
```json
{
  "status": "success",
  "tenant_id": "1",
  "total_payments": 5,
  "total_amount": 25000.0,
  "payments": [
    {
      "id": 1,
      "tenant_id": "1",
      "bill_id": 1,
      "amount": 5000.0,
      "payment_method": "bkash",
      "payment_date": "2026-01-15T10:30:00",
      "reference": "TXN123456",
      "created_at": "2026-01-15T10:30:00"
    }
  ]
}
```

**Status Codes:**
- ✅ `200` = Success (endpoint working)
- ❌ `404` = Not deployed OR tenant not found
- ❌ `500` = Server error

---

### 5️⃣ PAYMENT SUMMARY

**Endpoint:** `GET /api/payments/summary/{tenant_id}`

**Test Steps:**
1. Click on `GET /api/payments/summary/{tenant_id}`
2. Click "Try it out"
3. Enter `tenant_id`: `1`
4. Click "Execute"

**Expected Result:**
```json
{
  "status": "success",
  "tenant_id": "1",
  "summary": {
    "total_paid": 25000.0,
    "payment_count": 5,
    "average_payment": 5000.0,
    "payment_methods": {
      "bkash": 3,
      "cash": 2
    }
  }
}
```

**Status Codes:**
- ✅ `200` = Success
- ❌ `404` = Not deployed OR tenant not found

---

### 6️⃣ AGORA TOKEN STATUS

**Endpoint:** `GET /api/agora/status`

**Test Steps:**
1. Scroll to `agora` section
2. Click on `GET /api/agora/status`
3. Click "Try it out"
4. Click "Execute"

**Expected Result:**
```json
{
  "status": "configured",
  "app_id_configured": true,
  "certificate_configured": true,
  "sdk_installed": true,
  "token_expiration": 3600
}
```

**Status Codes:**
- ✅ `200` = Agora configured correctly
- ❌ `500` = Credentials missing

---

### 7️⃣ AGORA TOKEN GENERATION

**Endpoint:** `GET /api/agora/token/{channel}/{uid}`

**Test Steps:**
1. Click on `GET /api/agora/token/{channel}/{uid}`
2. Click "Try it out"
3. Enter:
   - `channel`: `test-room`
   - `uid`: `1001`
   - `role`: `publisher` (default)
4. Click "Execute"

**Expected Result:**
```json
{
  "status": "success",
  "token": "006eJ...[long token string]...HcA=",
  "channel": "test-room",
  "uid": 1001,
  "expires_in": 3600
}
```

**Status Codes:**
- ✅ `200` = Token generated (Agora working!)
- ❌ `500` = Agora SDK not installed or credentials wrong

---

## 📊 CHECKLIST

After testing all endpoints, fill this checklist:

| # | Endpoint | Status | Notes |
|---|----------|--------|-------|
| 1 | POST /api/tenants/approve/{id} | ☐ 200 ☐ 404 ☐ 500 | |
| 2 | POST /api/otp/send | ☐ 200 ☐ 404 ☐ 500 | |
| 3 | POST /api/otp/verify | ☐ 200 ☐ 400 ☐ 404 | |
| 4 | GET /api/payments/tenant/{id} | ☐ 200 ☐ 404 ☐ 500 | |
| 5 | GET /api/payments/summary/{id} | ☐ 200 ☐ 404 ☐ 500 | |
| 6 | GET /api/agora/status | ☐ 200 ☐ 500 | |
| 7 | GET /api/agora/token/{channel}/{uid} | ☐ 200 ☐ 500 | |

---

## 🎯 INTERPRETING RESULTS

### ✅ All Endpoints Return 200
**Status:** DEPLOYMENT SUCCESSFUL!

**Next Steps:**
1. ✅ Rebuild Flutter APK (already running)
2. ✅ Install APK on device
3. ✅ Test real flows in app

---

### ❌ Some Endpoints Return 404
**Status:** DEPLOYMENT INCOMPLETE

**Fix:**
1. Check Render dashboard: https://dashboard.render.com
2. Verify deployment logs
3. Wait for build to complete
4. Try again in 2-3 minutes

---

### ❌ Endpoints Return 500
**Status:** BACKEND ERROR

**Fix:**
1. Check Render logs for error details
2. Verify environment variables (Agora credentials)
3. Check database connection
4. Review error message in response body

---

## 🔍 TROUBLESHOOTING

### Problem: Swagger docs not loading
**Solution:**
- Backend not deployed or crashed
- Check: https://dashboard.render.com
- Wait for deployment to complete

### Problem: Only some endpoints show 404
**Solution:**
- New routers not registered in main_prod.py
- Check git commit included all files
- Redeploy: `git push origin main`

### Problem: Agora token returns 500
**Solution:**
- Check .env variables on Render:
  - `AGORA_APP_ID`
  - `AGORA_APP_CERTIFICATE`
- Verify agora-token-builder package installed
- Check deployment logs

### Problem: OTP send returns error
**Solution:**
- Check database `otp_codes` table exists
- Verify phone number format (should be: 017XXXXXXXX)
- Check database connection in Render logs

---

## 📱 AFTER SWAGGER TESTS PASS

### 1. Check Flutter APK Build Status
```powershell
# Already building in background
# Will complete in 2-3 minutes
```

### 2. Test from Flutter App
Open app and test:
- ✅ Login with OTP
- ✅ View payments
- ✅ Approve tenant (if owner)
- ✅ Start video call

### 3. Check Debug Logs
In Flutter console, look for:
```
🔵 CALLING: POST https://lifeasy-api.onrender.com/api/...
🟢 RESPONSE STATUS: 200
🟢 RESPONSE BODY: {...}
```

---

## 🎉 SUCCESS CRITERIA

All these must be true:

- [ ] Swagger docs load: https://lifeasy-api.onrender.com/docs
- [ ] POST /api/tenants/approve returns 200
- [ ] POST /api/otp/send returns 200
- [ ] POST /api/otp/verify returns 200 or 400 (400 is OK for invalid OTP)
- [ ] GET /api/payments/tenant/1 returns 200
- [ ] GET /api/agora/status returns 200
- [ ] GET /api/agora/token/test/1001 returns 200
- [ ] Flutter APK builds successfully
- [ ] APK installs on device
- [ ] App connects to backend

---

**TEST STARTED:** 2026-04-16  
**SWAGGER URL:** https://lifeasy-api.onrender.com/docs  
**APK BUILD:** In Progress
