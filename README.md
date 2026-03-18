# LIFEASY V30 PRO - Live Backend API

Production-ready FastAPI backend for LIFEASY apartment management system.

## 🚀 Deploy to Render

### Step 1: Initialize Git
```powershell
cd "E:\SUNNY\Jewel\APPERTMENT SOFTWER\lifeasy_backend_live"
git init
git add .
git commit -m "LIFEASY V30 PRO initial commit"
git branch -M main
```

### Step 2: Connect to GitHub
```powershell
git remote add origin https://github.com/YOUR_USERNAME/lifeasy-backend.git
git push -u origin main
```

### Step 3: Deploy on Render
1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Name**: lifeasy-backend
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

5. Click "Create Web Service"

## 📁 Files Included

- `main.py` - Main FastAPI application (Render-ready)
- `database.py` - Database configuration
- `models.py` - SQLAlchemy models
- `auth.py` - Authentication router
- `requirements.txt` - Python dependencies

## 🔧 Environment Variables (Optional)

Set these in Render dashboard if needed:
- `SECRET_KEY`: Your JWT secret key
- `DATABASE_URL`: Database connection string

## 📱 API Endpoints

- Home: `/`
- Health Check: `/health`
- Login: `/api/login`
- API Docs: `/docs`

## ⚠️ Important Notes

✅ No `if __name__ == "__main__"` block (Render incompatible)  
✅ Uses `$PORT` environment variable  
✅ SQLite database included  
✅ CORS enabled for mobile app  

## 🎯 Test Locally

```powershell
cd "E:\SUNNY\Jewel\APPERTMENT SOFTWER\lifeasy_backend_live"
.\.venv\Scripts\Activate.ps1
python -m uvicorn main:app --host 0.0.0.0 --port 8000
```

Visit: http://localhost:8000/docs
