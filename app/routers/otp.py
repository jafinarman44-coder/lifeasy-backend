from fastapi import APIRouter
from datetime import datetime, timedelta
import random

router = APIRouter(prefix="/api/otp", tags=["OTP"])

# In-memory store (later DB connect হবে)
OTP_STORE = {}

def generate_otp():
    return str(random.randint(100000, 999999))

@router.post("/send")
def send_otp(request: dict):
    tenant_id = request.get("tenant_id")

    if not tenant_id:
        return {"status": "error", "message": "Tenant ID required"}

    otp = generate_otp()
    expiry = datetime.utcnow() + timedelta(minutes=2)

    OTP_STORE[tenant_id] = {
        "otp": otp,
        "expiry": expiry
    }

    # 🔥 SMS integration later (bKash/Ssl/SMS gateway)
    print("OTP SENT:", otp)

    return {
        "status": "success",
        "message": "OTP sent successfully",
        "otp": otp      # ❗ Development mode only — flutter এর জন্য
    }

@router.post("/verify")
def verify_otp(request: dict):
    tenant_id = request.get("tenant_id")
    otp = request.get("otp")

    if tenant_id not in OTP_STORE:
        return {"status": "error", "message": "OTP not generated"}

    saved_otp = OTP_STORE[tenant_id]["otp"]
    expiry = OTP_STORE[tenant_id]["expiry"]

    if datetime.utcnow() > expiry:
        return {"status": "error", "message": "OTP expired"}

    if otp != saved_otp:
        return {"status": "error", "message": "Invalid OTP"}

    return {
        "status": "success",
        "message": "OTP verified successfully"
    }
