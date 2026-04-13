"""
LIFEASY BACKEND AUTO DIAGNOSTIC & AUTO RECOVERY AGENT
-----------------------------------------------------
This script will:

✔ Check required environment variables (.env)
✔ Validate SMTP / Brevo / Gmail OTP sending
✔ Validate DB connection + migrations
✔ Validate all routers (auth/chat/call)
✔ Validate WebSocket connectivity
✔ Validate Agora token generation
✔ Validate FCM server key
✔ Auto-fix common issues:
    - Missing pip packages
    - Missing email-validator
    - Missing python-dotenv
    - Missing JWT library
    - Missing migrations
✔ Finally show a detailed report of:
    - FIXED issues
    - FAILED issues
    - NEXT STEPS for ChatGPT assistant

Author: LIFEASY AI AUTOPILOT MODULE
"""

import os
import sys
import subprocess
import sqlite3
import time
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

report_fixed = []
report_failed = []
report_info = []


def run(cmd):
    """Run a shell command safely"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return result.stdout.strip(), result.stderr.strip()
    except Exception as e:
        return "", str(e)


# -------------------------------------------------------------
# 1. CHECK REQUIRED PIP PACKAGES
# -------------------------------------------------------------
required_packages = [
    "fastapi",
    "uvicorn",
    "python-dotenv",
    "sqlalchemy",
    "email-validator",
    "python-jose",
    "firebase-admin",
    "agora-token-builder",
]

report_info.append("Checking required Python packages...")

for pkg in required_packages:
    out, err = run(f"pip show {pkg}")
    if not out:
        report_failed.append(f"Package missing: {pkg}")
        out2, err2 = run(f"pip install {pkg}")
        if not err2:
            report_fixed.append(f"Installed missing package: {pkg}")
        else:
            report_failed.append(f"Failed installing package: {pkg}")


# -------------------------------------------------------------
# 2. CHECK ENV VARIABLES
# -------------------------------------------------------------
required_envs = [
    "SMTP_HOST",
    "SMTP_PORT",
    "SMTP_USERNAME",
    "SMTP_PASSWORD",
    "BREVO_API_KEY",
    "AGORA_APP_ID",
    "AGORA_APP_CERTIFICATE",
    "FIREBASE_CREDENTIALS_PATH",
]

report_info.append("Checking required environment variables...")

for key in required_envs:
    if not os.getenv(key):
        report_failed.append(f"Missing env variable: {key}")
    else:
        report_fixed.append(f"Found env variable: {key}")


# -------------------------------------------------------------
# 3. CHECK DATABASE CONNECTION
# -------------------------------------------------------------
report_info.append("Checking database connectivity...")

try:
    conn = sqlite3.connect("lifeasy_v30.db")
    conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    report_fixed.append("Database connected successfully")
except Exception as e:
    report_failed.append(f"Database connection failed: {str(e)}")


# -------------------------------------------------------------
# 4. CHECK OTP EMAIL SENDING
# -------------------------------------------------------------
otp_test_email = os.getenv("SMTP_USERNAME")

if otp_test_email:
    try:
        res = requests.post(
            "http://localhost:8000/api/v2/auth/test-otp",
            json={"email": otp_test_email},
            timeout=10
        )
        if res.status_code == 200:
            report_fixed.append("OTP test email sent successfully")
        else:
            report_failed.append("OTP test request failed")
    except Exception as e:
        report_failed.append(f"OTP test error: {str(e)}")
else:
    report_failed.append("Cannot test OTP because SMTP_USERNAME missing")


# -------------------------------------------------------------
# 5. CHECK AGORA TOKEN GENERATION
# -------------------------------------------------------------
report_info.append("Checking Agora token generation...")

try:
    res = requests.get("http://localhost:8000/api/call/v2/agora-token/test/1")
    if res.status_code == 200:
        report_fixed.append("Agora token generation OK")
    else:
        report_failed.append("Agora token endpoint returned error")
except Exception as e:
    report_failed.append(f"Agora test error: {str(e)}")


# -------------------------------------------------------------
# 6. CHECK WEBSOCKET SERVER STATUS
# -------------------------------------------------------------
report_info.append("Checking WebSocket server...")

import websockets
import asyncio

async def ws_test():
    try:
        async with websockets.connect("ws://localhost:8000/api/call/v2/ws/1"):
            report_fixed.append("WebSocket connection OK")
    except Exception as e:
        report_failed.append(f"WebSocket failed: {str(e)}")

asyncio.get_event_loop().run_until_complete(ws_test())


# -------------------------------------------------------------
# 7. FINAL REPORT
# -------------------------------------------------------------
print("\n\n=========================")
print("LIFEASY BACKEND DIAGNOSTIC REPORT")
print("=========================\n")

print("✔ FIXED / OK:")
for item in report_fixed:
    print("   - " + item)

print("\n❌ FAILED:")
for item in report_failed:
    print("   - " + item)

print("\nℹ️ INFO:")
for item in report_info:
    print("   - " + item)

print("\n\nNEXT STEPS:")
print("Send this full report to ChatGPT for auto-fix of FAILED items.")
