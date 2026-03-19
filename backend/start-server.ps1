# FastAPI Backend Startup Script
# This script starts the FastAPI server with hot reload

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  LIFEASY V27 - FastAPI Backend Server" -ForegroundColor Green
Write-Host "========================================`n" -ForegroundColor Green

Write-Host "Starting FastAPI server..." -ForegroundColor Yellow
Write-Host "Host: 0.0.0.0 (All network interfaces)" -ForegroundColor Cyan
Write-Host "Port: 8000" -ForegroundColor Cyan
Write-Host "Mode: Development (Hot Reload Enabled)" -ForegroundColor Cyan
Write-Host "API Base URL: http://192.168.0.119:8000/api`n" -ForegroundColor Cyan

Write-Host "Press CTRL+C to stop the server`n" -ForegroundColor Gray

# Start the FastAPI server
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
