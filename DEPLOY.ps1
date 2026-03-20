# ============================================
# LIFEASY V30 PRO - DEPLOYMENT COMMANDS
# ============================================

# 🔥 STEP 1: Connect to GitHub (Replace YOUR_USERNAME)
git remote add origin https://github.com/jafinarman44-coder/lifeasy-backend.git

# 🔥 STEP 2: Push to GitHub
git push -u origin main

# 🔥 STEP 3: Deploy on Render
# 1. Go to https://render.com
# 2. Click "New +" → "Web Service"
# 3. Select repository: lifeasy-backend
# 4. Settings:
#    - Name: lifeasy-backend
#    - Build Command: pip install -r requirements.txt
#    - Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT

# ============================================
# ✅ ALTERNATIVE: One-Click Deploy Script
# ============================================

Write-Host "🚀 LIFEASY V30 PRO DEPLOYMENT" -ForegroundColor Cyan
Write-Host ""

# Add GitHub remote
$remote = Read-Host "Enter GitHub username (default: jafinarman44-coder)"
if ($remote -eq "") { $remote = "jafinarman44-coder" }

git remote add origin "https://github.com/$remote/lifeasy-backend.git" 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ GitHub remote added" -ForegroundColor Green
} else {
    Write-Host "⚠️ Remote may already exist" -ForegroundColor Yellow
}

# Push to GitHub
git push -u origin main
if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Code pushed to GitHub" -ForegroundColor Green
    Write-Host ""
    Write-Host "🎉 NEXT STEPS:" -ForegroundColor Cyan
    Write-Host "1. Go to https://render.com" -ForegroundColor White
    Write-Host "2. New + → Web Service" -ForegroundColor White
    Write-Host "3. Connect repository: lifeasy-backend" -ForegroundColor White
    Write-Host "4. Deploy!" -ForegroundColor White
} else {
    Write-Host "❌ Push failed. Check GitHub credentials." -ForegroundColor Red
}
