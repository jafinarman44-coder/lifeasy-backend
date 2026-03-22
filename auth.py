from fastapi import APIRouter
from pydantic import BaseModel
import random

router = APIRouter()

# ====== MODELS ======
class LoginRequest(BaseModel):
    tenant_id: str
    password: str

class OTPVerify(BaseModel):
    tenant_id: str
    otp: str

# ====== FAKE DB ======
users = {
    "1001": {
        "password": "123456",
        "phone": "01700000000"
    }
}

otp_store = {}

# ====== LOGIN ======
@router.post("/login")
def login(data: LoginRequest):
    user = users.get(data.tenant_id)

    if not user or user["password"] != data.password:
        return {"status": "error", "message": "Invalid credentials"}

    otp = str(random.randint(100000, 999999))
    otp_store[data.tenant_id] = otp

    print("OTP:", otp)

    return {
        "status": "otp_sent",
        "otp": otp  # 🔥 remove in real production
    }

# ====== VERIFY OTP ======
@router.post("/verify-otp")
def verify_otp(data: OTPVerify):
    real_otp = otp_store.get(data.tenant_id)

    if real_otp != data.otp:
        return {"status": "error", "message": "Invalid OTP"}

    return {
        "status": "success",
        "message": "Login successful"
    }
