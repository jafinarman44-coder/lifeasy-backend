"""
LIFEASY V30 - OTP and Payment Endpoints
Missing endpoints for mobile app
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database_prod import get_db, SessionLocal as ProdSessionLocal
from models import OTPCode, Payment, Tenant
from auth_master import create_access_token, generate_otp, hash_password, verify_password
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import Optional, List
import random

router = APIRouter()

# ============================================
# 📱 PYDANTIC MODELS
# ============================================
class OTPSendRequest(BaseModel):
    phone: str

class OTPVerifyRequest(BaseModel):
    phone: str
    otp: str

class PaymentResponse(BaseModel):
    id: int
    tenant_id: str
    bill_id: Optional[int] = None
    amount: float
    payment_method: str
    payment_date: str
    reference: Optional[str] = None
    created_at: str

    class Config:
        from_attributes = True

# ============================================
# 🔐 OTP ENDPOINTS
# ============================================
@router.post("/otp/send")
async def send_otp(request: OTPSendRequest, db: Session = Depends(get_db)):
    """
    Send OTP to phone number.
    Generates 6-digit OTP and saves to database.
    """
    try:
        phone = request.phone.strip()
        
        if not phone:
            raise HTTPException(status_code=400, detail="Phone number is required")
        
        # Generate 6-digit OTP
        otp_code = generate_otp()
        
        # Set expiration time (5 minutes from now)
        expires_at = datetime.utcnow() + timedelta(minutes=5)
        
        # Check if this is for password reset or registration
        existing_tenant = db.query(Tenant).filter(Tenant.phone == phone).first()
        is_password_reset = existing_tenant is not None
        
        # Save OTP to database
        otp_record = OTPCode(
            email=phone,  # Using email field for phone
            otp=otp_code,
            expires_at=expires_at,
            is_used=False,
            is_password_reset=is_password_reset,
            created_at=datetime.utcnow()
        )
        
        db.add(otp_record)
        db.commit()
        db.refresh(otp_record)
        
        # In production, send SMS here
        # For now, log OTP (remove in production)
        print(f"🔔 OTP for {phone}: {otp_code}")
        
        return {
            "status": "success",
            "message": "OTP sent successfully",
            "phone": phone,
            "expires_in": 300  # 5 minutes in seconds
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to send OTP: {str(e)}"
        )

@router.post("/otp/verify")
async def verify_otp_endpoint(request: OTPVerifyRequest, db: Session = Depends(get_db)):
    """
    Verify OTP and return JWT token.
    Validates OTP from database and creates authentication token.
    """
    try:
        phone = request.phone.strip()
        otp = request.otp.strip()
        
        if not phone or not otp:
            raise HTTPException(status_code=400, detail="Phone and OTP are required")
        
        # Find the most recent unused OTP for this phone
        otp_record = db.query(OTPCode).filter(
            OTPCode.email == phone,
            OTPCode.otp == otp,
            OTPCode.is_used == False
        ).order_by(OTPCode.created_at.desc()).first()
        
        if not otp_record:
            raise HTTPException(
                status_code=400,
                detail="Invalid OTP"
            )
        
        # Check if OTP is expired
        if otp_record.expires_at and otp_record.expires_at < datetime.utcnow():
            raise HTTPException(
                status_code=400,
                detail="OTP has expired"
            )
        
        # Mark OTP as used
        otp_record.is_used = True
        db.commit()
        
        # Find or create tenant
        tenant = db.query(Tenant).filter(Tenant.phone == phone).first()
        
        if not tenant:
            # Create new tenant with auto-approval
            tenant = Tenant(
                name=f"User_{phone[-4:]}",  # Default name
                phone=phone,
                email=f"{phone}@lifeasy.app",  # Temporary email
                is_verified=True,
                is_active=True,
                created_at=datetime.utcnow()
            )
            db.add(tenant)
            db.commit()
            db.refresh(tenant)
        
        # Create JWT token
        access_token = create_access_token(
            data={
                "sub": str(tenant.id),
                "phone": tenant.phone,
                "tenant_id": str(tenant.tenant_id) if tenant.tenant_id else str(tenant.id)
            }
        )
        
        return {
            "status": "success",
            "message": "OTP verified successfully",
            "access_token": access_token,
            "token_type": "bearer",
            "tenant_id": str(tenant.tenant_id) if tenant.tenant_id else str(tenant.id),
            "phone": tenant.phone,
            "name": tenant.name,
            "expires_in": 43200  # 30 days in seconds
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to verify OTP: {str(e)}"
        )

# ============================================
# 💰 PAYMENT ENDPOINTS
# ============================================
@router.get("/payments/tenant/{tenant_id}")
async def get_tenant_payments(
    tenant_id: str,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """
    Get all payments for a tenant.
    Returns list of payments ordered by date (newest first).
    """
    try:
        # Verify tenant exists
        tenant = db.query(Tenant).filter(
            (Tenant.id == int(tenant_id)) | (Tenant.tenant_id == tenant_id)
        ).first()
        
        if not tenant:
            raise HTTPException(
                status_code=404,
                detail=f"Tenant {tenant_id} not found"
            )
        
        # Query payments
        payments = db.query(Payment).filter(
            (Payment.tenant_id == str(tenant.id)) | 
            (Payment.tenant_id == tenant.tenant_id)
        ).order_by(
            Payment.created_at.desc()
        ).offset(skip).limit(limit).all()
        
        # Format response
        result = []
        for payment in payments:
            result.append({
                "id": payment.id,
                "tenant_id": payment.tenant_id,
                "bill_id": payment.bill_id,
                "amount": payment.amount,
                "payment_method": payment.payment_method,
                "payment_date": payment.payment_date.isoformat() if payment.payment_date else None,
                "reference": payment.reference,
                "created_at": payment.created_at.isoformat() if payment.created_at else None
            })
        
        return {
            "status": "success",
            "tenant_id": tenant_id,
            "total_payments": len(result),
            "total_amount": sum(p["amount"] for p in result),
            "payments": result
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get payments: {str(e)}"
        )

@router.get("/payments/summary/{tenant_id}")
async def get_payment_summary(tenant_id: str, db: Session = Depends(get_db)):
    """
    Get payment summary for a tenant.
    Returns total paid, pending, and payment statistics.
    """
    try:
        # Find tenant
        tenant = db.query(Tenant).filter(
            (Tenant.id == int(tenant_id)) | (Tenant.tenant_id == tenant_id)
        ).first()
        
        if not tenant:
            raise HTTPException(
                status_code=404,
                detail=f"Tenant {tenant_id} not found"
            )
        
        # Get payment statistics
        payments = db.query(Payment).filter(
            (Payment.tenant_id == str(tenant.id)) | 
            (Payment.tenant_id == tenant.tenant_id)
        ).all()
        
        total_paid = sum(p.amount for p in payments)
        payment_count = len(payments)
        
        # Get payment methods breakdown
        methods = {}
        for p in payments:
            method = p.payment_method
            methods[method] = methods.get(method, 0) + 1
        
        return {
            "status": "success",
            "tenant_id": tenant_id,
            "summary": {
                "total_paid": total_paid,
                "payment_count": payment_count,
                "average_payment": total_paid / payment_count if payment_count > 0 else 0,
                "payment_methods": methods
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get payment summary: {str(e)}"
        )
