# 📧 LIFEASY SMTP TESTER - COMPLETE GUIDE

## 🎯 WHAT THIS DOES

This powerful script tests your **entire email delivery system**:
- ✅ Loads SMTP credentials from `.env`
- ✅ Validates configuration
- ✅ Tests backend connectivity
- ✅ Sends real OTP email
- ✅ Shows detailed error messages if anything fails
- ✅ Provides troubleshooting steps automatically

---

## 🚀 HOW TO RUN

### **Step 1: Open Terminal**
```powershell
cd "E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\backend"
```

### **Step 2: Run the Tester**
```powershell
.\test_smtp.ps1
```

### **Step 3: Enter Your Email**
The script will prompt:
```
Enter email address to receive test OTP
```

Type your Gmail address (or any email you want to test with).

---

## ✅ EXPECTED SUCCESS OUTPUT

If everything works correctly, you'll see:

```
========================================
  🎉 SUCCESS! OTP SENT!
========================================

📧 Check your email inbox:
   To: your_email@gmail.com
   Subject: Your LIFEASY OTP Code

📋 Backend Response:
{
    "status": "success",
    "message": "OTP sent successfully"
}

✅ EMAIL DELIVERY TEST PASSED!

Next Steps:
  1. Check your email inbox (and spam folder)
  2. Look for email with subject: 'Your LIFEASY OTP Code'
  3. Verify the 6-digit OTP code
  4. Use it to complete registration
```

**Then check your email!** You should receive:
- **Subject:** Your LIFEASY OTP Code
- **Body:** Your verification OTP is: 123456

---

## ❌ IF IT FAILS - AUTOMATIC TROUBLESHOOTING

The script automatically detects errors and provides specific fixes!

### **Error 1: 500 Internal Server Error**

**What you'll see:**
```
❌ SMTP TEST FAILED!
HTTP Status: 500
```

**Automatic fix instructions:**
```
⚠️  500 Internal Server Error detected!
    This usually means SMTP authentication failed.

✅ ACTION STEPS:
    1. Verify Gmail App Password (not regular password!)
    2. Go to: https://myaccount.google.com/apppasswords
    3. Create new App Password for 'Mail' on 'Windows Computer'
    4. Copy the 16-character password (remove spaces)
    5. Update .env: SMTP_PASSWORD=xxxxxxxxxxxxxxxx
    6. Restart backend server
    7. Run this test again
```

**How to fix:**
1. Visit https://myaccount.google.com/apppasswords
2. Sign in to majadar1din@gmail.com
3. Enable 2FA if not already enabled
4. Create App Password → Select "Mail" and "Windows Computer"
5. Google shows: `xkfp zytd wqrb pmac`
6. Remove spaces: `xfkpzytdwqrbpmac`
7. Update `.env`:
   ```
   SMTP_PASSWORD=xfkpzytdwqrbpmac
   ```
8. Restart backend:
   ```powershell
   Stop-Process -Name python -Force
   python -m uvicorn main_prod:app --host 0.0.0.0 --port 8000
   ```
9. Run test again: `.\test_smtp.ps1`

---

### **Error 2: Backend Not Running**

**What you'll see:**
```
❌ Backend server is not responding!
```

**Fix:**
```powershell
python -m uvicorn main_prod:app --host 0.0.0.0 --port 8000
```

Wait for "Backend ready!" message, then run test again.

---

### **Error 3: Missing Environment Variables**

**What you'll see:**
```
❌ ERROR: Missing required environment variables:
  - SMTP_EMAIL
  - SMTP_PASSWORD
```

**Fix:**
Open `.env` file and ensure these lines exist:
```
SMTP_EMAIL=majadar1din@gmail.com
SMTP_PASSWORD=your_16_digit_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

---

### **Error 4: Email Already Exists**

**What you'll see:**
```
HTTP Status: 400
{"status": "error", "message": "Email already exists"}
```

**Fix:**
Use a different email address for testing. The system prevents duplicate registrations.

---

## 🔍 WHAT THE SCRIPT CHECKS

### **Phase 1: Environment Loading**
- ✅ Checks if `.env` file exists
- ✅ Reads all SMTP configuration values
- ✅ Displays loaded configuration
- ✅ Validates required variables

### **Phase 2: Backend Health Check**
- ✅ Pings `/health` endpoint
- ✅ Verifies server is running
- ✅ Confirms database connection

### **Phase 3: OTP Request**
- ✅ Sends POST request to `/api/auth/v2/register-request`
- ✅ Includes test email, password, name, phone
- ✅ Handles response or error

### **Phase 4: Result Analysis**
- ✅ Parses JSON response
- ✅ Identifies success vs error
- ✅ Provides specific troubleshooting based on error type
- ✅ Shows actionable next steps

---

## 📊 TESTING WORKFLOW

```
1. Run Script
   ↓
2. Load .env
   ↓
3. Validate Config
   ↓
4. Test Backend Health
   ↓
5. Send OTP Request
   ↓
6. Receive Response
   ↓
7a. SUCCESS → Check email inbox
7b. ERROR → Automatic troubleshooting guide
```

---

## 🎯 COMPLETE TEST SEQUENCE

### **Before Running:**
1. ✅ Backend server running on port 8000
2. ✅ `.env` file configured with SMTP credentials
3. ✅ Internet connection active
4. ✅ Gmail App Password generated

### **Run Test:**
```powershell
.\test_smtp.ps1
```

### **During Test:**
- Watch for configuration display
- Enter test email when prompted
- Wait for backend response (2-5 seconds)

### **After Test:**

**If SUCCESS:**
- Check email inbox immediately
- Check spam/junk folder if not in inbox
- Look for subject: "Your LIFEASY OTP Code"
- Note the 6-digit OTP code

**If ERROR:**
- Read the detailed error message
- Follow automatic troubleshooting steps
- Fix the identified issue
- Run test again

---

## 🔧 MANUAL SMTP CONFIGURATION

### **Get Gmail App Password:**

1. **Visit:** https://myaccount.google.com/apppasswords
2. **Sign in** to: majadar1din@gmail.com
3. **Enable 2FA** (if not already):
   - Go to Security → 2-Step Verification
   - Follow setup process
4. **Generate App Password:**
   - Click "App passwords"
   - Select app: **Mail**
   - Select device: **Windows Computer**
   - Click **Generate**
5. **Copy Password:**
   - Google shows: `xkfp zytd wqrb pmac`
   - Remove ALL spaces: `xfkpzytdwqrbpmac`
   - This is your SMTP_PASSWORD

### **Update .env File:**

Open: `E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\backend\.env`

Set these values:
```
SMTP_EMAIL=majadar1din@gmail.com
SMTP_PASSWORD=xfkpzytdwqrbpmac
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
```

**Save the file.**

### **Restart Backend:**

```powershell
# Stop current server
Stop-Process -Name python -Force

# Start fresh
python -m uvicorn main_prod:app --host 0.0.0.0 --port 8000
```

Wait for: `✅ Backend ready!`

### **Run Test Again:**

```powershell
.\test_smtp.ps1
```

---

## 📧 EMAIL YOU SHOULD RECEIVE

**From:** majadar1din@gmail.com  
**To:** [your test email]  
**Subject:** Your LIFEASY OTP Code  

**Body:**
```
Your verification OTP is: 123456

This OTP was sent for LIFEASY registration.
If you didn't request this, please ignore this email.
```

The OTP code (123456) is randomly generated each time and valid for 10 minutes.

---

## 🎉 SUCCESS VERIFICATION

You know it worked when:

1. ✅ Script shows: "🎉 SUCCESS! OTP SENT!"
2. ✅ You receive email within 1-2 minutes
3. ✅ Email contains 6-digit OTP code
4. ✅ Backend console shows successful email send

**Backend Console Output (when successful):**
```
INFO: 127.0.0.1:xxxxx - "POST /api/auth/v2/register-request HTTP/1.1" 200 OK
```

---

## 💡 PRO TIPS

### **Tip 1: Use Real Email**
Test with an actual email you can access, not fake addresses.

### **Tip 2: Check Spam Folder**
Gmail sometimes marks automated emails as spam initially.

### **Tip 3: Multiple Tests**
Run multiple times with different emails to ensure stability.

### **Tip 4: Monitor Backend Logs**
Watch the backend console while running the test for real-time feedback.

### **Tip 5: Save Successful Config**
Once it works, backup your `.env` file as reference.

---

## 🚨 COMMON ISSUES & SOLUTIONS

| Issue | Solution |
|-------|----------|
| 500 Error | Wrong SMTP password - get new App Password |
| Backend not responding | Start server: `python -m uvicorn main_prod:app --host 0.0.0.0 --port 8000` |
| Email not received | Check spam folder, wait 2-3 minutes |
| "Email already exists" | Use different email address |
| Connection timeout | Check internet connection |
| .env not found | Ensure you're in backend directory |

---

## 📞 SUPPORT CONTACTS

If issues persist after following all steps:

**Check Backend Logs:**
- Watch terminal where backend is running
- Look for detailed error stack traces

**Google Account Help:**
- https://support.google.com/accounts/answer/185833

**Gmail SMTP Settings:**
- Server: smtp.gmail.com
- Port: 587 (TLS) or 465 (SSL)
- Requires App Password (not regular password)

---

## ✅ FINAL CHECKLIST

Before declaring success:

- [ ] `.env` file exists with all SMTP values
- [ ] Backend server running without errors
- [ ] Script runs without crashes
- [ ] Email received in inbox
- [ ] OTP code visible in email
- [ ] Can use OTP to verify registration

---

**STATUS: READY FOR TESTING!**  
**Script Location:** `E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\backend\test_smtp.ps1`  
**Next Action:** Run `.\test_smtp.ps1` and enter your email! 🚀
