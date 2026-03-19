# 🎯 RENDER START COMMAND - QUICK FIX

## ✅ COPY-PASTE THIS COMMAND

### For Render Dashboard → Settings → Build & Deploy:

```bash
uvicorn backend.main_prod:app --host 0.0.0.0 --port $PORT
```

---

## ⚠️ DON'T USE THESE:

❌ `cd backend && uvicorn main_prod:app ...` (may fail)  
❌ `uvicorn main:app ...` (wrong app - PyQt6 desktop!)  
❌ `uvicorn main_prod:app ...` (won't find module from root)

---

## 🔧 ALTERNATIVE OPTIONS

### Option 1: Using new file (also works)
```bash
uvicorn api_main:app --host 0.0.0.0 --port $PORT
```

### Option 2: If you have __init__.py in backend/
```bash
cd backend && uvicorn main_prod:app --host 0.0.0.0 --port $PORT
```

---

## 📋 STEPS TO DEPLOY

1. **Go to Render Dashboard**
   ```
   https://dashboard.render.com/
   ```

2. **Select your service**
   ```
   lifeasy-api
   ```

3. **Settings → Build & Deploy**

4. **Replace Start Command with:**
   ```bash
   uvicorn backend.main_prod:app --host 0.0.0.0 --port $PORT
   ```

5. **Click "Save Changes"**

6. **Manual Deploy → "Deploy latest commit"**

7. **Wait 2-5 minutes**

---

## ✅ EXPECTED LOGS

```
🚀 Starting LIFEASY V30 PRO...
✅ Backend ready!
Uvicorn running on http://0.0.0.0:PORT
Application startup complete.
```

---

## 🧪 TEST IT WORKS

### Visit:
```
https://lifeasy-api.onrender.com/docs
```

### Try endpoint:
```
POST /api/register
{
  "phone": "+8801712345678",
  "password": "test123"
}
```

### Should return:
```json
{
  "access_token": "eyJhbGc...",
  "tenant_id": "TNT17123456",
  "phone": "+8801712345678"
}
```

---

## 🐛 IF IT FAILS

### Error: "Module not found"
**Solution:** Make sure `backend/__init__.py` exists

### Error: "Can't find module"
**Solution:** Use full path: `backend.main_prod`

### Error: "Import failed"
**Solution:** Check all dependencies in requirements.txt

---

## 🎯 WHY THIS COMMAND?

✅ Works from root directory  
✅ No need for `cd backend`  
✅ Clear module path  
✅ All imports work correctly  
✅ Professional structure  

---

**Use this command and it will work!** 🚀
