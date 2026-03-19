from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from auth import create_token

router = APIRouter()

class LoginRequest(BaseModel):
    tenant_id: str
    password: str

@router.post("/login")
def login(data: LoginRequest):
    """Tenant login endpoint"""
    # Demo authentication - replace with actual DB query
    if data.tenant_id == "1001" and data.password == "123456":
        token = create_token({"tenant_id": data.tenant_id})
        return {
            "token": token,
            "tenant_id": data.tenant_id,
            "name": "Demo Tenant"
        }
    raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/send-otp")
def send_otp(data: dict):
    """Send OTP to tenant phone"""
    # Demo OTP - replace with actual SMS service
    return {"otp": "123456", "message": "OTP sent successfully"}

@router.post("/verify-otp")
def verify_otp(data: dict):
    """Verify OTP code"""
    otp = data.get("otp")
    if otp == "123456":
        return {"status": "verified", "message": "OTP verified successfully"}
    raise HTTPException(status_code=400, detail="Invalid OTP")
