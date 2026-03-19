# LIFEASY V28 ULTRA - Backend Server Startup Script
# Production Ready Server Launcher

$PROJECT = "E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27"

Write-Host ""
Write-Host "╔════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  LIFEASY V28 ULTRA - BACKEND SERVER   ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

Set-Location "$PROJECT\backend"

Write-Host "[1/3] Activating virtual environment..." -ForegroundColor Yellow
.\.venv\Scripts\Activate.ps1

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Failed to activate virtual environment!" -ForegroundColor Red
    Write-Host "Please ensure .venv folder exists in backend directory" -ForegroundColor Gray
    pause
    exit 1
}

Write-Host "✓ Virtual environment activated" -ForegroundColor Green
Write-Host ""

Write-Host "[2/3] Checking dependencies..." -ForegroundColor Yellow
python -c "import fastapi, uvicorn, sqlalchemy" 2>$null

if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing dependencies..." -ForegroundColor Gray
    pip install -r requirements.txt
}

Write-Host "✓ Dependencies verified" -ForegroundColor Green
Write-Host ""

Write-Host "[3/3] Starting FastAPI server..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Server will be available at:" -ForegroundColor Cyan
Write-Host "  • Local:    http://localhost:8000" -ForegroundColor White
Write-Host "  • Network:  http://192.168.0.119:8000" -ForegroundColor White
Write-Host "  • API Docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host ""
Write-Host "Press CTRL+C to stop the server" -ForegroundColor Gray
Write-Host ""

# Start the server
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
