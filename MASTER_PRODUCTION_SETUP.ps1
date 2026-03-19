# ============================================
# 🔥 LIFEASY V30 PRO - MASTER PRODUCTION SETUP
# Complete Installation & Deployment Script
# ============================================

Write-Host "🚀 LIFEASY V30 PRO - MASTER PRODUCTION SETUP" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# ============================================
# STEP 1: BACKEND PACKAGE INSTALLATION
# ============================================
Write-Host "⚡ STEP 1: Installing Backend Packages..." -ForegroundColor Yellow

Set-Location -Path "$PSScriptRoot\backend"

# Install Python packages
pip install fastapi uvicorn sqlalchemy passlib[bcrypt] python-jose requests twilio firebase-admin httpx psycopg2-binary python-dotenv gunicorn

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Backend packages installed successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Backend package installation failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""

# ============================================
# STEP 2: ENVIRONMENT CONFIGURATION
# ============================================
Write-Host "⚡ STEP 2: Setting up Environment Configuration..." -ForegroundColor Yellow

# Copy example env file if .env doesn't exist
if (-not (Test-Path ".env")) {
    Copy-Item ".env.example" -Destination ".env"
    Write-Host "⚠️ Created .env file - UPDATE WITH YOUR PRODUCTION CREDENTIALS!" -ForegroundColor Yellow
    Write-Host "   Edit backend\.env with your Twilio, bKash, Nagad, Firebase credentials" -ForegroundColor Yellow
} else {
    Write-Host "✅ .env file already exists" -ForegroundColor Green
}

Write-Host ""

# ============================================
# STEP 3: DATABASE INITIALIZATION
# ============================================
Write-Host "⚡ STEP 3: Initializing Database..." -ForegroundColor Yellow

# Set environment variable for production
$env:LIFEASY_ENV = "production"

# Initialize database
python -c "from database_prod import init_db; init_db()"

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Database initialized successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Database initialization failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""

# ============================================
# STEP 4: FIREBASE CONFIGURATION
# ============================================
Write-Host "⚡ STEP 4: Checking Firebase Configuration..." -ForegroundColor Yellow

if (-not (Test-Path "firebase_credentials.json")) {
    Write-Host "⚠️ Firebase credentials not found!" -ForegroundColor Yellow
    Write-Host "   Download firebase_credentials.json from Firebase Console" -ForegroundColor Yellow
    Write-Host "   Place it in backend/ directory" -ForegroundColor Yellow
} else {
    Write-Host "✅ Firebase credentials found" -ForegroundColor Green
}

Write-Host ""

# ============================================
# STEP 5: FLUTTER DEPENDENCIES
# ============================================
Write-Host "⚡ STEP 5: Installing Flutter Dependencies..." -ForegroundColor Yellow

Set-Location -Path "$PSScriptRoot\mobile_app"

# Get Flutter dependencies
flutter pub get

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Flutter dependencies installed successfully!" -ForegroundColor Green
} else {
    Write-Host "❌ Flutter dependencies installation failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""

# ============================================
# STEP 6: BUILD FLUTTER APK
# ============================================
Write-Host "⚡ STEP 6: Building Flutter APK..." -ForegroundColor Yellow

# Clean build
flutter clean

# Get dependencies again
flutter pub get

# Build release APK
flutter build apk --release

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ APK built successfully!" -ForegroundColor Green
    Write-Host "   APK Location: mobile_app/build/app/outputs/flutter-apk/app-release.apk" -ForegroundColor Cyan
} else {
    Write-Host "❌ APK build failed!" -ForegroundColor Red
}

Write-Host ""

# ============================================
# STEP 7: START BACKEND SERVER
# ============================================
Write-Host "⚡ STEP 7: Starting Backend Server..." -ForegroundColor Yellow

Set-Location -Path "$PSScriptRoot\backend"

# Start server in background
Write-Host "🌐 Starting server on http://0.0.0.0:8000" -ForegroundColor Cyan
Write-Host "📖 API Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""

# For production deployment (Render, Heroku, etc.)
# uvicorn main_prod:app --host 0.0.0.0 --port $PORT

# For local development
uvicorn main_prod:app --host 0.0.0.0 --port 8000 --reload

Write-Host ""
Write-Host "=============================================" -ForegroundColor Green
Write-Host "✅ LIFEASY V30 PRO SETUP COMPLETE!" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green
Write-Host ""
Write-Host "📱 MOBILE APP:" -ForegroundColor Cyan
Write-Host "   Install APK: build/app/outputs/flutter-apk/app-release.apk" -ForegroundColor White
Write-Host ""
Write-Host "🌐 BACKEND:" -ForegroundColor Cyan
Write-Host "   API URL: http://localhost:8000" -ForegroundColor White
Write-Host "   API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "🔧 NEXT STEPS:" -ForegroundColor Yellow
Write-Host "   1. Update backend/.env with production credentials" -ForegroundColor White
Write-Host "   2. Configure Twilio SMS credentials" -ForegroundColor White
Write-Host "   3. Configure bKash/Nagad payment gateway" -ForegroundColor White
Write-Host "   4. Setup Firebase Cloud Messaging" -ForegroundColor White
Write-Host "   5. Deploy to Render/Heroku/AWS" -ForegroundColor White
Write-Host ""
Write-Host "🎉 HAPPY CODING!" -ForegroundColor Green
Write-Host ""
