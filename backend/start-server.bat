@echo off
REM LIFEASY Backend Server Startup Script

echo ========================================
echo   LIFEASY V30 PRO - Backend Server
echo ========================================
echo.

cd /d "E:\SUNNY\Jewel\APPERTMENT SOFTWER\LIFEASY_V27\backend"

echo [1/3] Activating virtual environment...
call ..\..\ .venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment!
    pause
    exit /b 1
)
echo ✓ Virtual environment activated
echo.

echo [2/3] Checking .env file...
if not exist .env (
    echo WARNING: .env file not found!
    echo Please create .env with SMTP credentials first.
    pause
) else (
    echo ✓ .env file found
    echo.
    echo Current SMTP configuration:
    findstr /C:"SMTP_EMAIL=" .env
    findstr /C:"SMTP_PASSWORD=" .env
    findstr /C:"SMTP_SERVER=" .env
    findstr /C:"SMTP_PORT=" .env
)
echo.

echo [3/3] Starting backend server...
echo.
echo ========================================
echo   Server will start on:
echo   http://localhost:8000
echo   API Docs: http://localhost:8000/docs
echo ========================================
echo.
echo Press Ctrl+C to stop the server
echo.

python -m uvicorn main_prod:app --reload

pause
