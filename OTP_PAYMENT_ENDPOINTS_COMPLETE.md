# ✅ MISSING ENDPOINTS CREATED - COMPLETE

## 📋 WHAT WAS CREATED

### 1. ✅ New Router File: `otp_payment_router.py`

**File:** `backend/routers/otp_payment_router.py`

This router contains all 3 missing endpoints with proper error handling and JWT integration.

---

## 🔐 ENDPOINT 1: POST /api/otp/send

**Purpose:** Generate and send 6-digit OTP to phone number

### Request Body:
```json
{
  "phone": "01717574875"
}
```

### Success Response (200):
```json
{
  "status": "success",
  "message": "OTP sent successfully",
  "phone": "01717574875",
  "expires_in": 300
}
```

### Features:
- ✅ Generates random 6-digit OTP
- ✅ Saves to `otp_codes` table with 5-minute expiry
- ✅ Detects if phone exists (password reset vs registration)
- ✅ Proper error handling (try/except)
- ✅ In production: Sends SMS via Twilio/SSL Wireless
- ✅ Development mode: Logs OTP to console

### Implementation:
```python
@router.post("/otp/send")
async def send_otp(request: OTPSendRequest, db: Session = Depends(get_db)):
    # Generate OTP
    otp_code = generate_otp()  # Returns random 6-digit code
    
    # Save to database
    otp_record = OTPCode(
        email=phone,
        otp=otp_code,
        expires_at=datetime.utcnow() + timedelta(minutes=5),
        is_used=False,
        is_password_reset=is_password_reset
    )
    
    db.add(otp_record)
    db.commit()
    
    return {"status": "success", ...}
```

---

## 🔐 ENDPOINT 2: POST /api/otp/verify

**Purpose:** Verify OTP and return JWT authentication token

### Request Body:
```json
{
  "phone": "01717574875",
  "otp": "123456"
}
```

### Success Response (200):
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

### Error Response (400):
```json
{
  "detail": "Invalid OTP"
}
```

### Features:
- ✅ Validates OTP from `otp_codes` table
- ✅ Checks expiration time
- ✅ Marks OTP as used after verification
- ✅ Auto-creates tenant if new user
- ✅ Generates JWT token with tenant info
- ✅ Returns complete auth payload

### Implementation:
```python
@router.post("/otp/verify")
async def verify_otp_endpoint(request: OTPVerifyRequest, db: Session = Depends(get_db)):
    # Find OTP in database
    otp_record = db.query(OTPCode).filter(
        OTPCode.email == phone,
        OTPCode.otp == otp,
        OTPCode.is_used == False
    ).first()
    
    # Check expiration
    if otp_record.expires_at < datetime.utcnow():
        raise HTTPException(status_code=400, detail="OTP has expired")
    
    # Mark as used
    otp_record.is_used = True
    db.commit()
    
    # Create JWT token
    access_token = create_access_token(data={
        "sub": str(tenant.id),
        "phone": tenant.phone,
        "tenant_id": tenant.tenant_id
    })
    
    return {"access_token": access_token, ...}
```

---

## 💰 ENDPOINT 3: GET /api/payments/tenant/{tenant_id}

**Purpose:** Get all payments for a tenant

### Request:
```
GET /api/payments/tenant/1
GET /api/payments/tenant/1?skip=0&limit=50
```

### Success Response (200):
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

### Features:
- ✅ Queries `payments` table
- ✅ Supports pagination (skip/limit)
- ✅ Orders by date (newest first)
- ✅ Returns payment statistics
- ✅ Works with tenant ID or database ID

### Implementation:
```python
@router.get("/payments/tenant/{tenant_id}")
async def get_tenant_payments(tenant_id: str, db: Session = Depends(get_db)):
    # Find tenant
    tenant = db.query(Tenant).filter(
        (Tenant.id == int(tenant_id)) | 
        (Tenant.tenant_id == tenant_id)
    ).first()
    
    # Query payments
    payments = db.query(Payment).filter(
        Payment.tenant_id == tenant.id
    ).order_by(Payment.created_at.desc()).all()
    
    return {
        "total_payments": len(payments),
        "total_amount": sum(p.amount for p in payments),
        "payments": [...]
    }
```

---

## 📊 BONUS ENDPOINT: GET /api/payments/summary/{tenant_id}

**Purpose:** Get payment summary and statistics

### Response:
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

---

## 🔧 HOW TO USE FROM MOBILE APP

### Example 1: Send OTP
```dart
final response = await http.post(
  Uri.parse('https://lifeasy-api.onrender.com/api/otp/send'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode({'phone': '01717574875'}),
);

final data = jsonDecode(response.body);
print('OTP sent: ${data['message']}');
```

### Example 2: Verify OTP and Get Token
```dart
final response = await http.post(
  Uri.parse('https://lifeasy-api.onrender.com/api/otp/verify'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode({
    'phone': '01717574875',
    'otp': '123456'
  }),
);

final data = jsonDecode(response.body);
final token = data['access_token'];
print('Token: $token');
```

### Example 3: Get Payments
```dart
final response = await http.get(
  Uri.parse('https://lifeasy-api.onrender.com/api/payments/tenant/1'),
);

final data = jsonDecode(response.body);
print('Total payments: ${data['total_payments']}');
print('Total amount: ${data['total_amount']}');
```

---

## 📂 FILES MODIFIED

### Created:
1. ✅ `backend/routers/otp_payment_router.py` - New router with all endpoints

### Modified:
2. ✅ `backend/main_prod.py` - Added router registration

---

## 🚀 DEPLOYMENT STEPS

### Step 1: Commit Changes
```bash
cd e:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\backend
git add .
git commit -m "Add OTP and Payment endpoints for mobile app"
git push origin main
```

### Step 2: Wait for Render Deploy (2-3 minutes)
Render will automatically deploy when you push to main branch.

### Step 3: Test Endpoints
```powershell
cd e:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\backend
.\test_new_endpoints.ps1
```

### Step 4: Verify on Swagger Docs
Visit: https://lifeasy-api.onrender.com/docs

Look for:
- `POST /api/otp/send`
- `POST /api/otp/verify`
- `GET /api/payments/tenant/{tenant_id}`
- `GET /api/payments/summary/{tenant_id}`

---

## 🧪 TESTING COMMANDS

### Test All New Endpoints:
```powershell
# Run comprehensive test
.\test_new_endpoints.ps1
```

### Manual Test with PowerShell:
```powershell
# Test OTP Send
$body = @{ phone = "01717574875" } | ConvertTo-Json
Invoke-WebRequest -Uri "https://lifeasy-api.onrender.com/api/otp/send" -Method POST -Body $body -ContentType "application/json"
```

### Test with cURL:
```bash
# Test OTP Send
curl -X POST https://lifeasy-api.onrender.com/api/otp/send \
  -H "Content-Type: application/json" \
  -d '{"phone": "01717574875"}'

# Test Payments
curl https://lifeasy-api.onrender.com/api/payments/tenant/1
```

---

## ✅ ERROR HANDLING

All endpoints include:

### 1. Input Validation:
```python
if not phone:
    raise HTTPException(status_code=400, detail="Phone number is required")
```

### 2. Database Error Handling:
```python
try:
    # Database operations
    db.commit()
except Exception as e:
    raise HTTPException(status_code=500, detail=f"Error: {str(e)}")
```

### 3. Not Found Errors:
```python
if not tenant:
    raise HTTPException(status_code=404, detail="Tenant not found")
```

### 4. Validation Errors:
```python
if otp_record.expires_at < datetime.utcnow():
    raise HTTPException(status_code=400, detail="OTP has expired")
```

---

## 🔒 SECURITY FEATURES

1. ✅ **OTP Expiration**: 5-minute expiry time
2. ✅ **Single Use**: OTP marked as used after verification
3. ✅ **JWT Tokens**: Secure authentication tokens
4. ✅ **Password Hashing**: Bcrypt for password storage
5. ✅ **SQL Injection Protection**: SQLAlchemy ORM
6. ✅ **Input Validation**: Pydantic models

---

## 📊 CURRENT STATUS

| Endpoint | Status | Description |
|----------|--------|-------------|
| `POST /api/otp/send` | ✅ Code Ready | Generate and send OTP |
| `POST /api/otp/verify` | ✅ Code Ready | Verify OTP and return JWT |
| `GET /api/payments/tenant/{id}` | ✅ Code Ready | Get tenant payments |
| `GET /api/payments/summary/{id}` | ✅ Code Ready | Payment statistics |
| `POST /api/tenants/approve/{id}` | ✅ Code Ready | Approve tenant (from previous fix) |

---

## ⏳ NEXT STEPS

1. **Deploy to Render** (2-3 minutes)
   ```bash
   git push origin main
   ```

2. **Test Endpoints**
   ```powershell
   .\test_new_endpoints.ps1
   ```

3. **Rebuild APK** (optional, if you want to include new endpoint integration)
   ```bash
   flutter build apk --release
   ```

4. **Test Full Flow**
   - OTP Send → OTP Verify → Get Token → Access Protected Endpoints

---

## 📞 TROUBLESHOOTING

### If endpoints still show 404:

1. **Check Render Dashboard:**
   - Visit: https://dashboard.render.com
   - Check deployment logs
   - Ensure build succeeded

2. **Check Router Registration:**
   - Verify `main_prod.py` includes the new router
   - Look for: `app.include_router(otp_payment_router)`

3. **Check Swagger Docs:**
   - Visit: https://lifeasy-api.onrender.com/docs
   - Search for `/otp/` and `/payments/`

4. **Check Logs:**
   ```powershell
   # Check if router imported
   curl https://lifeasy-api.onrender.com/api/health
   ```

---

## 🎯 COMPLETE FLOW EXAMPLE

### User Login with OTP:

1. **Send OTP:**
   ```
   POST /api/otp/send
   Body: {"phone": "01717574875"}
   Response: OTP sent successfully
   ```

2. **User receives OTP:** `123456`

3. **Verify OTP:**
   ```
   POST /api/otp/verify
   Body: {"phone": "01717574875", "otp": "123456"}
   Response: {"access_token": "eyJhbGci..."}
   ```

4. **Use Token:**
   ```
   GET /api/payments/tenant/1
   Headers: Authorization: Bearer eyJhbGci...
   ```

---

**CREATED:** 2026-04-16  
**BACKEND VERSION:** V30 PRO  
**STATUS:** ✅ Code Ready, Awaiting Deployment
