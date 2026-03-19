# 🚀 RENDER DEPLOYMENT - CORRECT START COMMANDS

## ✅ THREE WAYS TO RUN BACKEND ON RENDER

---

## 🔥 OPTION 1: Use backend/main_prod.py (RECOMMENDED)

### Start Command:
```bash
cd backend && uvicorn main_prod:app --host 0.0.0.0 --port $PORT
```

### OR (if cd doesn't work):
```bash
uvicorn backend.main_prod:app --host 0.0.0.0 --port $PORT
```

### Why This Works:
- ✅ Direct path to main_prod.py
- ✅ Uses production configuration
- ✅ All routers included
- ✅ No extra files needed

---

## 🔥 OPTION 2: Use New api_main.py (Root Level)

### Start Command:
```bash
uvicorn api_main:app --host 0.0.0.0 --port $PORT
```

### What This Does:
- Imports app from `backend/main_prod.py`
- Makes it accessible from root directory
- Cleaner for some deployment setups

### File Created:
```
api_main.py (in root directory)
```

---

## 🔥 OPTION 3: Rename/Copy main_prod.py to Root

### Option 3A: Copy to Root
```bash
# Copy backend/main_prod.py to root
cp backend/main_prod.py ./main.py
```

Then use:
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

### Option 3B: Create Symbolic Link
```bash
ln -s backend/main_prod.py main.py
```

Then use:
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
```

---

## ⚠️ IMPORTANT NOTES

### About Your Current main.py:

Your existing `main.py` is for **Desktop PyQt6 App**, NOT the backend API!

**Current main.py:**
```python
"""LIFEASY V27 - Desktop Admin Application"""
from PyQt6.QtWidgets import QApplication, QMainWindow...
```

This is for Windows desktop GUI, not for web backend.

**DO NOT replace it!** Keep both separate:
- `main.py` → Desktop app (PyQt6)
- `backend/main_prod.py` → Backend API (FastAPI)
- `api_main.py` → Root-level backend entry point (new)

---

## 🎯 RECOMMENDED RENDER SETUP

### Step 1: Choose Start Command

**Best Option:**
```bash
cd backend && uvicorn main_prod:app --host 0.0.0.0 --port $PORT
```

**Alternative (if cd fails):**
```bash
uvicorn backend.main_prod:app --host 0.0.0.0 --port $PORT
```

**Or use new file:**
```bash
uvicorn api_main:app --host 0.0.0.0 --port $PORT
```

### Step 2: Update Render Dashboard

1. Go to: https://dashboard.render.com/
2. Select: lifeasy-api
3. Settings → Build & Deploy
4. Change Start Command to one of above
5. Click "Save Changes"
6. Manual Deploy → "Deploy latest commit"

### Step 3: Verify Deployment

Check logs for:
```
🚀 Starting LIFEASY V30 PRO...
✅ Backend ready!
Uvicorn running on http://0.0.0.0:PORT
Application startup complete.
```

---

## 🧪 TEST YOUR DEPLOYMENT

### Test Endpoint:
```
https://lifeasy-api.onrender.com/health
```

**Expected Response:**
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

### Test API Docs:
```
https://lifeasy-api.onrender.com/docs
```

Should show Swagger UI with all endpoints.

---

## 🐛 TROUBLESHOOTING

### Error: "No module named 'main_prod'"

**Solution:**
Use full path:
```bash
uvicorn backend.main_prod:app --host 0.0.0.0 --port $PORT
```

### Error: "cd: can't cd to backend"

**Solution:**
Don't use cd, use module path:
```bash
uvicorn backend.main_prod:app --host 0.0.0.0 --port $PORT
```

### Error: "ModuleNotFoundError: No module named 'backend'"

**Solution:**
Make sure you have `__init__.py` in backend folder:
```bash
touch backend/__init__.py
git add .
git commit -m "Add __init__.py"
git push
```

### App starts but no routes work

**Check:**
1. Routers properly imported in main_prod.py
2. Include_router calls present
3. Check logs for import errors

---

## 📋 QUICK REFERENCE

### File Structure:
```
LIFEASY_V27/
├── main.py                    # Desktop PyQt6 app (NOT for backend)
├── api_main.py                # NEW: Root backend entry point
├── backend/
│   ├── __init__.py           # Make it a Python package
│   ├── main_prod.py          # Production FastAPI app
│   ├── auth_master.py        # Authentication
│   ├── payment_gateway.py    # Payments
│   └── notification_service.py # Notifications
```

### Start Commands (Choose ONE):

**Option A (Recommended):**
```bash
cd backend && uvicorn main_prod:app --host 0.0.0.0 --port $PORT
```

**Option B (If cd fails):**
```bash
uvicorn backend.main_prod:app --host 0.0.0.0 --port $PORT
```

**Option C (Using new file):**
```bash
uvicorn api_main:app --host 0.0.0.0 --port $PORT
```

**❌ WRONG (Don't Use):**
```bash
uvicorn main:app --host 0.0.0.0 --port $PORT
# This will try to run PyQt6 desktop app, not backend!
```

---

## ✅ VERIFICATION CHECKLIST

After deployment:

- [ ] Correct start command used
- [ ] No "cd backend" errors in logs
- [ ] Application startup complete message
- [ ] /health endpoint returns healthy status
- [ ] /docs shows Swagger UI
- [ ] Can test /api/register endpoint
- [ ] Can test /api/login endpoint
- [ ] Logs show debug prints

---

## 🎯 BEST PRACTICE

### For Render Deployment:

1. **Keep backend code in backend/ folder** ✅
2. **Use main_prod.py for production** ✅
3. **Create root-level entry point if needed** ✅
4. **Test locally before deploying** ✅
5. **Monitor logs after deployment** ✅

### Local Testing:

Before deploying, test locally:

```bash
# From root directory
uvicorn backend.main_prod:app --host 0.0.0.0 --port 8000 --reload

# OR using new file
uvicorn api_main:app --host 0.0.0.0 --port 8000 --reload
```

Visit: http://localhost:8000/docs

---

## 🎊 SUCCESS CRITERIA

### You know it's working when:

**Logs show:**
```
🚀 Starting LIFEASY V30 PRO...
✅ Backend ready!
Uvicorn running on http://0.0.0.0:PORT
Application startup complete.
```

**Endpoints respond:**
```
GET /health → {"status":"healthy"}
POST /api/register → Returns access_token
POST /api/login → Returns access_token
```

**No errors:**
```
❌ No "module not found" errors
❌ No "cd: can't cd" errors
❌ No import errors
```

---

## 📞 FINAL RECOMMENDATION

**For your case, use this start command on Render:**

```bash
uvicorn backend.main_prod:app --host 0.0.0.0 --port $PORT
```

**Why?**
- ✅ No need for `cd backend`
- ✅ Works from root directory
- ✅ Clear module path
- ✅ All imports will work
- ✅ Professional structure

**OR use the new file:**

```bash
uvicorn api_main:app --host 0.0.0.0 --port $PORT
```

Both will work perfectly! Choose one and stick with it.

---

**Last Updated:** 2026-03-20  
**Status:** ✅ Ready for Render Deployment  
**Files Created:** api_main.py (root-level entry point)
