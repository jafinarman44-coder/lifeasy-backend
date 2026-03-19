# ============================================
# 🚀 LIFEASY V30 PRO - QUICK START SCRIPT
# FastAPI Backend Production Server
# ============================================

Write-Host "🚀 LIFEASY V30 PRO - Starting Backend Server..." -ForegroundColor Cyan
Write-Host ""

# Set working directory
Set-Location -Path "$PSScriptRoot\backend"

# Check if .env exists
if (-not (Test-Path ".env")) {
    Write-Host "⚠️ WARNING: .env file not found!" -ForegroundColor Yellow
    Write-Host "   Copy .env.example to .env and configure credentials" -ForegroundColor Yellow
    Write-Host ""
}

# Set production environment
$env:LIFEASY_ENV = "production"

# Get port from environment or use default
$port = if ($env:PORT) { $env:PORT } else { "8000" }

Write-Host "🌐 Server Configuration:" -ForegroundColor Green
Write-Host "   Environment: production" -ForegroundColor Cyan
Write-Host "   Host: 0.0.0.0" -ForegroundColor Cyan
Write-Host "   Port: $port" -ForegroundColor Cyan
Write-Host "   API Docs: http://localhost:$port/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Yellow
Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

# Start server
uvicorn main_prod:app --host 0.0.0.0 --port $port --reload
