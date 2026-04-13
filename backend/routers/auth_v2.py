"""
LIFEASY V27+ PHASE 6 STEP 2 - Unified Cloud Registration System (V2)
Complete signup flow with owner approval workflow
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database_prod import get_db
from models import Tenant, OTPCode
from pydantic import BaseModel, EmailStr
from typing import Optional, List
import random
import hashlib
from datetime import datetime, timedelta
from jose import jwt
import os
from utils.email_service import send_otp_email
from utils.sms_service import sms_service
from models import ChatPresence
from datetime import datetime

router = APIRouter(prefix="/api/auth/v2", tags=["Authentication V2"])

# Configuration
SECRET_KEY_V2 = "lifeasy_phase6_v2_secret_key_2026_enterprise"
ALGORITHM_V2 = "HS256"


# ==================== PYDANTIC MODELS ====================

class RegisterRequestModel(BaseModel):
    email: EmailStr
    password: str
    phone: Optional[str] = ""
    name: str


class RegisterVerifyModel(BaseModel):
    email: EmailStr
    otp: str


class LoginV2RequestModel(BaseModel):
    email: EmailStr
    password: str
    remember_me: Optional[bool] = False


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    otp: str
    new_password: str


class TenantApprovalModel(BaseModel):
    tenant_id: int
    approved: bool
    building: Optional[str] = None
    floor: Optional[str] = None
    flat: Optional[str] = None
    start_date: Optional[str] = None


# ==================== HELPER FUNCTIONS ====================

def hash_password_v2(password: str) -> str:
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()


def verify_password_v2(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return hash_password_v2(plain_password) == hashed_password


def create_access_token_v2(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT token with V2 secret"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(hours=24))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY_V2, algorithm=ALGORITHM_V2)
    return encoded_jwt


def generate_otp() -> str:
    """Generate 6-digit OTP"""
    return str(random.randint(100000, 999999))


# ==================== REGISTRATION FLOW ====================

@router.post("/register-request")
def register_request(data: RegisterRequestModel, db: Session = Depends(get_db)):
    """
    Step 1: User enters name, email, password
    Step 2: We send OTP to email IF new user
    If user exists, we resend OTP for login
    """
    
    # 1. Check if email exists
    existing = db.query(Tenant).filter(Tenant.email == data.email).first()
    
    if existing:
        # Email exists - check if verified
        if not existing.is_verified:
            # Not verified yet - allow resending OTP
            pass  # Continue to send OTP
        else:
            # Already verified - user should login instead
            return {
                "status": "exists",
                "message": "Email already registered. Please login.",
                "is_verified": True,
                "needs_approval": not existing.is_active
            }

    # 2. Generate OTP
    otp = random.randint(100000, 999999)
    
    # 3. Set expiration (5 minutes from now)
    expires_at = datetime.utcnow() + timedelta(minutes=5)

    # 4. Save to OTP table with registration data
    record = OTPCode(
        email=data.email,
        otp=str(otp),
        created_at=datetime.utcnow(),
        expires_at=expires_at,
        name=data.name,
        phone=data.phone,
        password=data.password  # Will be hashed during verification
    )
    db.add(record)
    db.commit()

    # 5. Send OTP via EMAIL
    email_success = send_otp_email(data.email, str(otp))
    
    # 6. Send OTP via SMS (if phone provided)
    sms_success = True
    if data.phone and len(data.phone) >= 11:
        sms_success = sms_service.send_otp_sms(data.phone, str(otp))
        print(f"📱 SMS OTP sent to {data.phone}: {sms_success}")
    
    if not email_success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send OTP email"
        )

    return {
        "status": "success",
        "message": "OTP sent successfully via Email" + (" and SMS" if sms_success else ""),
        "delivery": {
            "email": email_success,
            "sms": sms_success
        }
    }


@router.post("/register-verify")
def register_verify(data: RegisterVerifyModel, db: Session = Depends(get_db)):
    """
    Step 2: Verify OTP
    - Validate OTP
    - Mark tenant as verified
    - Return tenant info + approval status
    """
    email = data.email
    otp = data.otp
    
    # Find OTP
    otp_record = db.query(OTPCode).filter(
        OTPCode.email == email,
        OTPCode.otp == otp,
        OTPCode.is_used == False
    ).first()
    
    if not otp_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "error",
                "message": "Invalid or expired OTP"
            }
        )
    
    # Check expiration
    if datetime.utcnow() > otp_record.expires_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "error",
                "message": "OTP expired. Please request a new one."
            }
        )
    
    # Mark OTP as used
    otp_record.is_used = True
    
    # Find tenant - if not exists, create it from stored registration data
    tenant = db.query(Tenant).filter(Tenant.email == email).first()
    
    if not tenant:
        # Create new tenant from stored registration data
        if not otp_record.name or not otp_record.password:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "status": "error",
                    "message": "Registration data missing. Please request a new OTP."
                }
            )
        
        # Hash password before storing
        hashed_password = hash_password_v2(otp_record.password)
        
        # Generate unique tenant_id
        import uuid
        generated_tenant_id = f"TENANT_{uuid.uuid4().hex[:8].upper()}"
        
        # Create tenant record with AUTO-APPROVAL
        tenant = Tenant(
            tenant_id=generated_tenant_id,
            name=otp_record.name,
            email=email,
            phone=otp_record.phone or "",
            password=hashed_password,
            is_verified=True,
            is_active=True,  # AUTO-APPROVE new users
            flat=None,  # Can be updated later
            building=None  # Can be updated later
        )
        db.add(tenant)
        db.commit()
        db.refresh(tenant)
    else:
        # Update existing tenant
        tenant.is_verified = True
    # Keep is_active=False until owner approves
    
    db.commit()
    
    # Determine response based on approval status
    if tenant.is_active:
        # Already approved (rare case)
        return {
            "status": "success",
            "message": "Registration complete! You can now login.",
            "tenant_id": tenant.id,
            "approval_status": "approved",
            "tenant": {
                "id": tenant.id,
                "name": tenant.name,
                "email": tenant.email,
                "phone": tenant.phone
            }
        }
    else:
        # Awaiting owner approval
        return {
            "status": "success",
            "message": "OTP verified! Awaiting owner approval.",
            "tenant_id": tenant.id,
            "approval_status": "pending",
            "tenant": {
                "id": tenant.id,
                "name": tenant.name,
                "email": tenant.email
            },
            "note": "You will be able to login once the property owner approves your registration."
        }


# ==================== LOGIN V2 ====================

@router.post("/login")
def login_v2(data: LoginV2RequestModel, db: Session = Depends(get_db)):
    """
    V2 Login with email and password
    Returns JWT token and full tenant profile
    """
    email = data.email
    password = data.password
    
    # Find tenant
    tenant = db.query(Tenant).filter(Tenant.email == email).first()
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "status": "error",
                "message": "Invalid credentials. Email not registered."
            }
        )
    
    # Verify password
    password_hash = hash_password_v2(password)
    print(f"🔑 Login attempt for {email}")
    print(f"   Provided password hash: {password_hash[:20]}...")
    print(f"   Stored password hash: {tenant.password[:20] if tenant.password else 'None'}...")
    
    if not verify_password_v2(password, tenant.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "status": "error",
                "message": "Invalid credentials. Wrong password."
            }
        )
    
    # Check verification status (defensive check for missing column)
    is_verified = getattr(tenant, 'is_verified', True)  # Default True if column missing
    if not is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "status": "error",
                "message": "Email not verified. Please complete OTP verification."
            }
        )
    
    # Check approval status FIRST
    is_active = getattr(tenant, 'is_active', True)  # Default True if column missing
    if not is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "status": "error",
                "message": "Account awaiting owner approval. Please contact the building administrator.",
                "approval_status": "pending",
                "tenant_id": tenant.id
            }
        )
    
    # Create JWT token
    token_expires = timedelta(days=7) if data.remember_me else timedelta(hours=24)
    access_token = create_access_token_v2(
        data={"sub": str(tenant.id), "email": tenant.email, "type": "tenant"},
        expires_delta=token_expires
    )
    
    # Update online status to 'online'
    presence = db.query(ChatPresence).filter(ChatPresence.user_id == tenant.id).first()
    if presence:
        presence.status = "online"
        presence.last_seen = datetime.utcnow()
    else:
        presence = ChatPresence(
            user_id=tenant.id,
            status="online",
            last_seen=datetime.utcnow()
        )
        db.add(presence)
    db.commit()
    
    print(f"✅ Login successful for {email}")
    print(f"🟢 User {tenant.id} marked as ONLINE")
    
    return {
        "status": "success",
        "message": "Login successful",
        "tenant_id": tenant.id,
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": int(token_expires.total_seconds()),
        "tenant": {
            "id": tenant.id,
            "name": tenant.name,
            "email": tenant.email,
            "phone": tenant.phone,
            "building": tenant.building,
            "floor": tenant.flat.split("-")[0] if "-" in str(tenant.flat) else "",
            "flat": tenant.flat,
            "is_verified": getattr(tenant, 'is_verified', True),
            "is_active": getattr(tenant, 'is_active', True)
        }
    }


# ==================== PROFILE MANAGEMENT ====================

@router.get("/my-profile")
def get_my_profile(
    tenant_id: int,
    db: Session = Depends(get_db)
):
    """
    Get current tenant profile
    Auto-fills all tenant details from cloud
    """
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status": "error",
                "message": "Tenant not found"
            }
        )
    
    # Extract floor from flat format (e.g., "3A" -> floor "3")
    floor = ""
    if tenant.flat:
        flat_str = str(tenant.flat)
        # Try to extract numeric part
        floor = ''.join(c for c in flat_str if c.isdigit())
    
    return {
        "status": "success",
        "profile": {
            "id": tenant.id,
            "name": tenant.name,
            "email": tenant.email,
            "phone": tenant.phone,
            "building": tenant.building or "",
            "floor": floor,
            "flat": tenant.flat or "",
            "start_date": tenant.created_at.isoformat() if tenant.created_at else "",
            "profile_photo": tenant.profile_photo or "",
            "is_verified": getattr(tenant, 'is_verified', True),
            "is_active": getattr(tenant, 'is_active', True)
        }
    }


# ==================== TOKEN REFRESH ====================

@router.get("/refresh-token")
def refresh_token(
    user_id: int,
    db: Session = Depends(get_db)
):
    """
    Refresh JWT token for authenticated user
    Returns new access token without requiring re-login
    """
    # Verify user exists and is active
    tenant = db.query(Tenant).filter(Tenant.id == user_id).first()
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status": "error",
                "message": "User not found"
            }
        )
    
    if not getattr(tenant, 'is_verified', True) or not getattr(tenant, 'is_active', True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                "status": "error",
                "message": "Account not active or verified"
            }
        )
    
    # Create new JWT token
    new_token = create_access_token_v2(
        data={"sub": str(tenant.id), "email": tenant.email, "type": "tenant"},
        expires_delta=timedelta(hours=24)
    )
    
    return {
        "status": "success",
        "token": new_token,
        "token_type": "bearer",
        "expires_in": 86400  # 24 hours in seconds
    }


# ==================== TENANT AUTO-FILL CHECK ====================

@router.get("/check-email/{email}")
def check_email_and_autofill(email: str, db: Session = Depends(get_db)):
    """
    Check if email exists in tenants table
    If exists, return building/floor/flat/name/phone automatically
    Used during signup to auto-fill details
    """
    tenant = db.query(Tenant).filter(Tenant.email == email).first()
    
    if not tenant:
        return {
            "status": "not_found",
            "message": "Email not registered in building"
        }
    
    # Extract floor from flat
    floor = ""
    if tenant.flat:
        flat_str = str(tenant.flat)
        floor = ''.join(c for c in flat_str if c.isdigit())
    
    return {
        "status": "found",
        "message": "Email registered in building",
        "tenant": {
            "id": tenant.id,
            "name": tenant.name,
            "phone": tenant.phone,
            "building": tenant.building or "",
            "floor": floor,
            "flat": tenant.flat or "",
            "start_date": tenant.created_at.isoformat() if tenant.created_at else "",
            "is_verified": getattr(tenant, 'is_verified', True),
            "is_active": getattr(tenant, 'is_active', True)
        }
    }


# ==================== OWNER APPROVAL WORKFLOW ====================

@router.get("/pending-tenants")
def get_pending_tenants(db: Session = Depends(get_db)):
    """
    Get all tenants awaiting approval
    Used by Windows App admin panel
    """
    pending = db.query(Tenant).filter(
        getattr(Tenant, 'is_verified', True) == True,
        getattr(Tenant, 'is_active', True) == False
    ).all()
    
    return {
        "status": "success",
        "count": len(pending),
        "tenants": [
            {
                "id": t.id,
                "name": t.name,
                "email": t.email,
                "phone": t.phone,
                "created_at": t.created_at.isoformat() if t.created_at else ""
            }
            for t in pending
        ]
    }


@router.post("/approve-tenant")
def approve_tenant(data: TenantApprovalModel, db: Session = Depends(get_db)):
    """
    Approve or reject tenant registration
    Used by Windows App owner/admin
    """
    tenant = db.query(Tenant).filter(Tenant.id == data.tenant_id).first()
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status": "error",
                "message": "Tenant not found"
            }
        )
    
    if data.approved:
        # Approve tenant
        tenant.is_active = True
        
        # Update property details if provided
        if data.building:
            tenant.building = data.building
        if data.floor:
            # Combine floor and flat if flat also provided
            if data.flat:
                tenant.flat = f"{data.floor}{data.flat}"
            else:
                tenant.flat = data.floor
        if data.start_date:
            # Could add a move_in_date field if needed
            pass
        
        db.commit()
        
        return {
            "status": "success",
            "message": "Tenant approved successfully",
            "tenant_id": tenant.id
        }
    else:
        # Reject tenant - optionally delete or keep as rejected
        # For now, we'll just mark as inactive permanently
        tenant.is_active = False
        db.commit()
        
        return {
            "status": "success",
            "message": "Tenant rejected",
            "tenant_id": tenant.id
        }


@router.delete("/reject-tenant/{tenant_id}")
def reject_tenant(tenant_id: int, db: Session = Depends(get_db)):
    """
    Delete rejected tenant
    """
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "error", "message": "Tenant not found"}
        )
    
    db.delete(tenant)
    db.commit()
    
    return {
        "status": "success",
        "message": "Tenant rejected and removed"
    }


# ==================== FORGOT PASSWORD FLOW ====================

@router.post("/forgot-password")
def forgot_password(data: ForgotPasswordRequest, db: Session = Depends(get_db)):
    """
    Step 1: User enters email for password reset
    Send OTP to their email
    """
    email = data.email
    
    # Check if email exists
    tenant = db.query(Tenant).filter(Tenant.email == email).first()
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status": "error",
                "message": "Email not found. Please register first."
            }
        )
    
    # Generate new OTP
    otp = random.randint(100000, 999999)
    expires_at = datetime.utcnow() + timedelta(minutes=5)
    
    # Save OTP record
    record = OTPCode(
        email=email,
        otp=str(otp),
        created_at=datetime.utcnow(),
        expires_at=expires_at,
        name=tenant.name,
        phone=tenant.phone or "",
        is_password_reset=True  # Mark as password reset, not registration
    )
    db.add(record)
    db.commit()
    
    # Send OTP via email
    email_success = send_otp_email(email, str(otp))
    
    # Send OTP via SMS if phone exists
    sms_success = True
    if tenant.phone and len(tenant.phone) >= 11:
        sms_success = sms_service.send_otp_sms(tenant.phone, str(otp))
    
    return {
        "status": "success",
        "message": "OTP sent to your email and phone",
        "delivery": {
            "email": email_success,
            "sms": sms_success
        }
    }


@router.post("/reset-password")
def reset_password(data: ResetPasswordRequest, db: Session = Depends(get_db)):
    """
    Step 2: Verify OTP and set new password
    For password reset, OTP is already verified (is_used=True), so we just need to find it
    """
    email = data.email
    otp = data.otp
    new_password = data.new_password
    
    # Find OTP record for password reset (can be already used since it was verified)
    otp_record = db.query(OTPCode).filter(
        OTPCode.email == email,
        OTPCode.otp == otp,
        OTPCode.is_password_reset == True
    ).order_by(OTPCode.created_at.desc()).first()
    
    if not otp_record:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "error",
                "message": "Invalid OTP. Please request a new password reset."
            }
        )
    
    # Check expiration (even if used, OTP must not be expired)
    if datetime.utcnow() > otp_record.expires_at:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "status": "error",
                "message": "OTP expired. Please request a new password reset."
            }
        )
    
    # Find tenant
    tenant = db.query(Tenant).filter(Tenant.email == email).first()
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "status": "error",
                "message": "User not found"
            }
        )
    
    # Update password
    tenant.password = hash_password_v2(new_password)
    db.commit()
    
    return {
        "status": "success",
        "message": "Password reset successful! You can now login with your new password."
    }
