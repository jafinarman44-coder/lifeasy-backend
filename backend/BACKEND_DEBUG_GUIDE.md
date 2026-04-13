# 🔧 LIFEASY V30 PRO - Backend Debugging Guide

## 📋 Quick Diagnostic Steps

### ✅ Step 1: Test Basic Connectivity
```powershell
# Open browser and test these URLs:
https://lifeasy-api.onrender.com/
https://lifeasy-api.onrender.com/health
https://lifeasy-api.onrender.com/api/status
```

**Expected Result:** JSON response with status "running" or "healthy"

**If you see error:**
- ❌ "Application Error" → Server crashed, check logs
- ❌ "Service Unavailable" → Server is down/sleeping
- ❌ "502 Bad Gateway" → Server crashed on startup

---

### ✅ Step 2: Run Automated Diagnostic Test

**Option A: PowerShell Script (Recommended)**
```powershell
cd "e:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\backend"
.\test_backend_diagnostic.ps1
```

**Option B: Python Script**
```powershell
cd "e:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\backend"
python test_api_diagnostic.py
```

**What it does:**
- Tests all critical endpoints
- Shows which ones pass/fail
- Provides detailed error messages
- Generates a test report

---

### ✅ Step 3: Check Render Live Logs

1. **Go to Render Dashboard:**
   - Visit: https://dashboard.render.com
   - Login to your account

2. **Select your web service:**
   - Click on "lifeasy-api" (or your service name)

3. **Open Logs tab:**
   - Click "Logs" in the left sidebar
   - You'll see real-time logs

4. **Trigger an API request:**
   - Open your app and try to login
   - Or visit: `https://lifeasy-api.onrender.com/api/auth/login`

5. **Watch for errors:**
   ```
   ERROR /api/login
   Traceback (most recent call last):
     File "...", line X, in ...
       ...
   Exception: Actual error message here
   ```

---

### ✅ Step 4: Enable Enhanced Error Logging

**Upload the debug version to Render:**

1. **Replace `main_prod.py` with `main_prod_debug.py`:**
   ```powershell
   # In your backend folder:
   cd "e:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\backend"
   
   # Backup current version
   cp main_prod.py main_prod_backup.py
   
   # Use debug version
   cp main_prod_debug.py main_prod.py
   ```

2. **Commit and push to Git:**
   ```powershell
   git add .
   git commit -m "Enable enhanced error logging"
   git push origin main
   ```

3. **Render will auto-deploy with new logging**

**What enhanced logging provides:**
- ✅ Full stack traces for all errors
- ✅ Request/response logging
- ✅ Database connection errors
- ✅ Detailed exception messages
- ✅ Timestamp for each error

---

### ✅ Step 5: Database Verification

**Problem:** Tables don't exist or database connection fails

**Check database connection:**

```python
# Create file: test_database.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
print(f"Database URL: {DATABASE_URL[:50]}...")

try:
    engine = create_engine(DATABASE_URL)
    with engine.connect() as conn:
        # Test connection
        result = conn.execute(text("SELECT 1"))
        print("✅ Database connection successful!")
        
        # Check tables
        result = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """))
        tables = [row[0] for row in result.fetchall()]
        print(f"\n📊 Found {len(tables)} tables:")
        for table in tables:
            print(f"   - {table}")
            
except Exception as e:
    print(f"❌ Database connection failed: {e}")
```

**Run it:**
```powershell
python test_database.py
```

---

## 🔍 Common Issues & Fixes

### Issue 1: Database Connection Failed
**Symptoms:**
```
ERROR: relation "tenants" does not exist
```

**Fix:**
```powershell
# Run database migrations
cd "e:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\backend"
python create_all_tables.py
```

**Or manually create tables via Render Shell:**
1. Go to Render Dashboard → Your Service → Shell
2. Run:
```bash
python create_all_tables.py
```

---

### Issue 2: Missing Environment Variables
**Symptoms:**
```
DATABASE_URL is not set
SECRET_KEY_V2 is missing
```

**Fix:**
1. Go to Render Dashboard → Your Service → Environment
2. Add all variables from `.env` file:
   - `LIFEASY_ENV=production`
   - `DATABASE_URL=postgresql://...`
   - `SECRET_KEY_V2=your_secret`
   - `BREVO_API_KEY=your_key`
   - etc.

---

### Issue 3: Import Errors
**Symptoms:**
```
ModuleNotFoundError: No module named 'xyz'
```

**Fix:**
```powershell
# Update requirements.txt
pip freeze > requirements.txt

# Or install missing package manually
pip install package_name

# Push to Render
git add requirements.txt
git commit -m "Add missing dependency"
git push
```

---

### Issue 4: Server Crashes on Startup
**Symptoms:**
- Render logs show: "Process exited with code 1"
- Health check fails

**Fix:**
```powershell
# Test locally first
cd "e:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\backend"
python main_prod_debug.py

# Look for errors in console
# Fix them before pushing to Render
```

---

### Issue 5: 500 Internal Server Error on Login
**Symptoms:**
```
POST /api/auth/login → 500 Error
```

**Debug Steps:**

1. **Check Render logs** - Look for:
   ```
   ERROR: Invalid email or password
   ERROR: Database query failed
   ERROR: JWT generation failed
   ```

2. **Test manually:**
   ```powershell
   # Using curl
   curl -X POST "https://lifeasy-api.onrender.com/api/auth/login" `
        -H "Content-Type: application/json" `
        -d '{"email":"test@example.com","password":"Test@123"}'
   ```

3. **Check database has users:**
   ```powershell
   python check_existing.py
   ```

---

## 🚀 Deploy Enhanced Logging Version

### Quick Deploy Commands:

```powershell
# 1. Navigate to backend folder
cd "e:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\backend"

# 2. Replace with debug version
cp main_prod_debug.py main_prod.py

# 3. Test locally
python main_prod.py

# 4. Commit and push
git add .
git commit -m "feat: enable enhanced error logging for debugging"
git push origin main

# 5. Wait for Render to deploy (2-3 minutes)
# 6. Check Render logs for detailed errors
```

---

## 📊 Diagnostic Checklist

Use this checklist to systematically debug:

- [ ] **Step 1:** Test `/health` endpoint - Is server running?
- [ ] **Step 2:** Run `test_backend_diagnostic.ps1` - Which endpoints fail?
- [ ] **Step 3:** Check Render logs - What errors appear?
- [ ] **Step 4:** Verify `DATABASE_URL` - Does it connect?
- [ ] **Step 5:** Check tables exist - Run `create_all_tables.py`
- [ ] **Step 6:** Verify env vars - All variables set in Render?
- [ ] **Step 7:** Test login manually - Does it work?
- [ ] **Step 8:** Check app requests - What API does app call?

---

## 🎯 Next Actions

After running diagnostics:

1. **If server is down:**
   - Check Render logs for startup errors
   - Verify all dependencies in `requirements.txt`
   - Test locally with `python main_prod.py`

2. **If specific endpoint fails:**
   - Check Render logs when hitting that endpoint
   - Look for database errors
   - Verify route is included in `main_prod.py`

3. **If all endpoints work but app fails:**
   - Check CORS settings
   - Verify app is using correct API URL
   - Check request headers in app

4. **If database issues:**
   - Run `python create_all_tables.py`
   - Verify PostgreSQL connection string
   - Check Render database is active

---

## 📞 Quick Commands Reference

```powershell
# Test connectivity
curl https://lifeasy-api.onrender.com/health

# Run diagnostic
.\test_backend_diagnostic.ps1

# Test specific endpoint
python -c "import requests; print(requests.get('https://lifeasy-api.onrender.com/health').json())"

# Check database
python test_database.py

# Run server locally
python main_prod_debug.py

# View logs (if using Render CLI)
render logs -s lifeasy-api
```

---

## 🔥 Emergency Fix - Redeploy Everything

If nothing works:

```powershell
# 1. Go to backend folder
cd "e:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\backend"

# 2. Use debug version
cp main_prod_debug.py main_prod.py

# 3. Commit everything
git add .
git commit -m "fix: emergency redeploy with enhanced logging"

# 4. Push to Render
git push origin main

# 5. Go to Render dashboard
# 6. Click "Manual Deploy" → "Clear build cache & deploy"
# 7. Watch logs for errors
```

---

## 📝 What to Share if You Need Help

When asking for help, provide:

1. **Render logs** (last 50 lines when error occurs)
2. **Diagnostic report** (from `test_backend_diagnostic.ps1`)
3. **Specific endpoint** that's failing
4. **Error message** from app or browser
5. **Database status** (tables exist? connection works?)

---

**Last Updated:** 2026-04-14
**Version:** V30.0.0
