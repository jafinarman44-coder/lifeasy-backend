"""
LIFEASY V27+ PHASE 6 - Complete Auth System
OTP-based authentication, login, profile management
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database_prod import get_db
from models import Tenant, OTPCode
from pydantic import BaseModel
from typing import Optional
import random
import hashlib
from datetime import datetime, timedelta
from jose import jwt

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

SECRET_KEY = "lifeasy_phase6_secret_key_2026"
ALGORITHM = "HS256"

# Email sending (configure with your SMTP)
SMTP_EMAIL = "majadar1din@gmail.com"
SMTP_PASSWORD = "your_app_password_here"


def hash_password(password: str) -> str:
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return hash_password(plain_password) == hashed_password


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create JWT token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(hours=24))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def send_email(email: str, otp: str):
    """Send OTP via email (implement with smtplib or email service)"""
    # TODO: Implement actual email sending
    # For now, just log it
    print(f"📧 Sending OTP {otp} to {email}")
    # Use smtplib or SendGrid/Resend API here
    pass


class SendOTPRequest(BaseModel):
    email: str


class VerifyOTPRequest(BaseModel):
    email: str
    otp: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str
    remember_me: Optional[bool] = False


@router.post("/send-otp")
async def send_otp(data: SendOTPRequest, db: Session = Depends(get_db)):
    """
    Send OTP to tenant email for signup/verification
    """
    email = data.email
    
    # Check if tenant exists by email
    tenant = db.query(Tenant).filter(Tenant.email == email).first()
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "error", "message": "Email not registered"}
        )
    
    # Generate 6-digit OTP
    otp = str(random.randint(100000, 999999))
    
    # Set expiration time (5 minutes)
    expires_at = datetime.utcnow() + timedelta(minutes=5)
    
    # Save OTP to database
    otp_record = OTPCode(
        email=email,
        otp=otp,
        expires_at=expires_at,
        is_used=False
    )
    db.add(otp_record)
    db.commit()
    
    # Send email with OTP
    try:
        await send_email(email, otp)
        
        return {
            "status": "success",
            "message": "OTP sent successfully to your email",
            "email": email
        }
    except Exception as e:
        db.delete(otp_record)
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"status": "error", "message": f"Failed to send email: {str(e)}"}
        )


@router.post("/verify")
def verify_otp(data: VerifyOTPRequest, db: Session = Depends(get_db)):
    """
    Verify OTP and set password
    Returns tenant_id on success
    """
    email = data.email
    otp = data.otp
    password = data.password
    
    # Find unused OTP for this email
    otp_record = db.query(OTPCode).filter(
        OTPCode.email == email,
        OTPCode.otp == otp,
        OTPCode.is_used == False
    ).first()
    
    if not otp_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"status": "error", "message": "Invalid OTP"}
        )
    
    # Check if OTP is expired
    if datetime.utcnow() > otp_record.expires_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"status": "error", "message": "OTP expired"}
        )
    
    # Mark OTP as used
    otp_record.is_used = True
    db.commit()
    
    # Update tenant password and verification status
    tenant = db.query(Tenant).filter(Tenant.email == email).first()
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "error", "message": "Tenant not found"}
        )
    
    tenant.password = hash_password(password)
    tenant.is_verified = True
    db.commit()
    
    # Return tenant info
    return {
        "status": "success",
        "message": "Email verified successfully",
        "tenant_id": tenant.id,
        "tenant": {
            "id": tenant.id,
            "name": tenant.name,
            "email": tenant.email
        }
    }


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """
    Tenant login with email and password
    """
    email = data.email
    password = data.password
    
    # Find tenant by email
    tenant = db.query(Tenant).filter(Tenant.email == email).first()
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"status": "error", "message": "Invalid credentials"}
        )
    
    # Verify password
    if not verify_password(password, tenant.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"status": "error", "message": "Invalid credentials"}
        )
    
    # Check if account is active
    if not tenant.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={"status": "error", "message": "Account inactive. Contact support."}
        )
    
    # Create JWT token
    token_expires = timedelta(days=7) if data.remember_me else timedelta(hours=24)
    access_token = create_access_token(
        data={"sub": str(tenant.id), "email": tenant.email},
        expires_delta=token_expires
    )
    
    return {
        "status": "success",
        "message": "Login successful",
        "tenant_id": tenant.id,
        "access_token": access_token,
        "token_type": "bearer",
        "tenant": {
            "id": tenant.id,
            "name": tenant.name,
            "email": tenant.email,
            "phone": tenant.phone,
            "is_verified": tenant.is_verified,
            "is_active": tenant.is_active
        }
    }


@router.get("/profile/{tenant_id}")
def get_profile(tenant_id: int, db: Session = Depends(get_db)):
    """
    Get tenant profile information
    Auto-fills name, building, floor, flat, photo
    """
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "error", "message": "Tenant not found"}
        )
    
    return {
        "status": "success",
        "profile": {
            "id": tenant.id,
            "name": tenant.name,
            "mobile": tenant.phone,
            "email": tenant.email,
            "building": tenant.building,
            "floor": tenant.flat.split("-")[0] if "-" in tenant.flat else "",  # Extract from flat format
            "flat": tenant.flat,
            "start_date": tenant.created_at.isoformat() if tenant.created_at else None,
            "photo": tenant.profile_photo,
            "is_verified": tenant.is_verified,
            "is_active": tenant.is_active
        }
    }


@router.put("/profile/{tenant_id}")
def update_profile(tenant_id: int, profile_data: dict, db: Session = Depends(get_db)):
    """
    Update tenant profile (photo, phone, etc.)
    """
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "error", "message": "Tenant not found"}
        )
    
    # Update fields
    if "name" in profile_data:
        tenant.name = profile_data["name"]
    if "phone" in profile_data:
        tenant.phone = profile_data["phone"]
    if "profile_photo" in profile_data:
        tenant.profile_photo = profile_data["profile_photo"]
    
    db.commit()
    db.refresh(tenant)
    
    return {
        "status": "success",
        "message": "Profile updated successfully",
        "profile": {
            "id": tenant.id,
            "name": tenant.name,
            "email": tenant.email,
            "phone": tenant.phone,
            "profile_photo": tenant.profile_photo
        }
    }
