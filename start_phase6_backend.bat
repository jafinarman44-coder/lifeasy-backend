@echo off
REM =====================================================
REM LIFEASY V27+ PHASE 6 - Quick Start Script
REM Runs database migration and starts backend server
REM =====================================================

echo.
echo ========================================
echo   LIFEASY V27+ PHASE 6 STARTUP
echo ========================================
echo.

REM Step 1: Run database migration
echo [1/3] Running database migration...
cd /d "%~dp0backend"
python db_migrate_phase6.py
if errorlevel 1 (
    echo.
    echo ERROR: Database migration failed!
    echo Please check the error message above.
    pause
    exit /b 1
)
echo.

REM Step 2: Start backend server
echo [2/3] Starting backend server...
echo.
echo ========================================
echo   BACKEND SERVER STARTING...
echo ========================================
echo.
echo API Documentation: http://localhost:8000/docs
echo Health Check: http://localhost:8000/health
echo.

uvicorn main_prod:app --host 0.0.0.0 --port 8000 --reload

if errorlevel 1 (
    echo.
    echo ERROR: Backend server failed to start!
    pause
    exit /b 1
)

echo.
echo [3/3] Server stopped.
echo.
pause
