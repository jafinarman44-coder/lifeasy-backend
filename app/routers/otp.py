from fastapi import APIRouter
import random
from fastapi_mail import MessageSchema
from app.core.email_config import fm

router = APIRouter(prefix="/api/otp", tags=["OTP"])

# In-memory store (later DB connect হবে)
OTP_STORAGE = {}

# Tenant email mapping (later DB থেকে আসবে)
TENANT_EMAIL = {
    "1001": "your_email_here@gmail.com"
}

@router.post("/send")
async def send_otp(data: dict):
    tenant_id = data.get("tenant_id")
    password = data.get("password")

    if not tenant_id:
        return {"status": "error", "message": "Tenant ID required"}

    # Check if tenant exists in email database
    if tenant_id not in TENANT_EMAIL:
        return {"status": "error", "message": "Email not found for this tenant"}

    otp = random.randint(100000, 999999)
    OTP_STORAGE[tenant_id] = otp

    # Send email with OTP
    try:
        message = MessageSchema(
            subject="Your LIFEASY Login OTP",
            recipients=[TENANT_EMAIL[tenant_id]],
            body=f"Your LIFEASY Login OTP is: {otp}\n\nThis OTP is valid for single use.",
            subtype="plain"
        )

        await fm.send_message(message)
        
        print(f"OTP sent to {TENANT_EMAIL[tenant_id]}: {otp}")
        
        return {
            "status": "success",
            "message": "OTP sent to your email",
            "email": TENANT_EMAIL[tenant_id]  # For frontend display
        }
    except Exception as e:
        print(f"Email send error: {str(e)}")
        return {"status": "error", "message": f"Failed to send email: {str(e)}"}

@router.post("/verify")
def verify_otp(data: dict):
    tenant_id = data.get("tenant_id")
    otp = data.get("otp")

    if tenant_id not in OTP_STORAGE:
        return {"status": "error", "message": "OTP not generated"}

    if str(otp) != str(OTP_STORAGE[tenant_id]):
        return {"status": "error", "message": "Invalid OTP"}

    return {
        "status": "success",
        "message": "OTP verified successfully"
    }
