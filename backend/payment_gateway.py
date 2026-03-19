"""
LIFEASY V30 PRO - Payment Gateway Integration
bKash & Nagad Payment Processing (Bangladesh)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database_prod import get_db
from models import Tenant, Payment
from jose import jwt
from pydantic import BaseModel
from datetime import datetime
import os
import httpx
import uuid

router = APIRouter()

# ============================================
# 💳 PAYMENT CONFIGURATION
# ============================================
BKASH_BASE_URL = os.getenv("BKASH_BASE_URL", "https://checkout.sandbox.bka.sh/v1.2.0-beta")
BKASH_APP_KEY = os.getenv("BKASH_APP_KEY")
BKASH_APP_SECRET = os.getenv("BKASH_APP_SECRET")
BKASH_USERNAME = os.getenv("BKASH_USERNAME")
BKASH_PASSWORD = os.getenv("BKASH_PASSWORD")

NAGAD_BASE_URL = os.getenv("NAGAD_BASE_URL", "https://api.sandbox.nagad-payment.com")
NAGAD_MERCHANT_ID = os.getenv("NAGAD_MERCHANT_ID")
NAGAD_API_KEY = os.getenv("NAGAD_API_KEY")


# ============================================
# 🔐 PAYMENT MODELS
# ============================================
class PaymentCreateRequest(BaseModel):
    tenant_id: str
    amount: float
    description: str = "Rent Payment"
    payment_method: str = "bkash"  # bkash or nagad

class PaymentExecuteRequest(BaseModel):
    payment_id: str
    transaction_id: str

class PaymentResponse(BaseModel):
    success: bool
    message: str
    payment_url: str = None
    transaction_id: str = None
    payment_id: str = None


# ============================================
# 🔧 BKASH SERVICE
# ============================================
class BkashService:
    """bKash Payment Gateway Service"""
    
    @staticmethod
    async def get_token() -> str:
        """Get bKash authorization token"""
        url = f"{BKASH_BASE_URL}/tokenized/authorize/token"
        
        headers = {
            "username": BKASH_USERNAME,
            "password": BKASH_PASSWORD,
            "app_key": BKASH_APP_KEY,
            "app_secret": BKASH_APP_SECRET,
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("id_token")
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"bKash token failed: {response.status_code}"
                )
    
    @staticmethod
    async def create_payment(tenant_id: str, amount: float, description: str, db: Session) -> dict:
        """Create bKash payment"""
        token = await BkashService.get_token()
        
        url = f"{BKASH_BASE_URL}/tokenized/checkout/create"
        
        # Get tenant details
        tenant = db.query(Tenant).filter(Tenant.tenant_id == tenant_id).first()
        if not tenant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tenant not found"
            )
        
        # Unique payment ID
        payment_id = f"PAY{uuid.uuid4().hex[:12].upper()}"
        
        payload = {
            "mode": "0011",
            "callbackURL": f"https://your-api-url.com/api/payment/bkash/callback/{payment_id}",
            "amount": str(amount),
            "currency": "BDT",
            "intent": "sale",
            "merchantInvoiceNumber": payment_id
        }
        
        headers = {
            "Authorization": token,
            "X-App-Key": BKASH_APP_KEY,
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                # Store payment record
                payment = Payment(
                    tenant_id=tenant_id,
                    amount=amount,
                    payment_method="bkash",
                    payment_id=payment_id,
                    transaction_id=data.get("transactionID"),
                    status="pending",
                    payment_date=datetime.utcnow()
                )
                db.add(payment)
                db.commit()
                
                return {
                    "success": True,
                    "payment_url": data.get("bkashURL"),
                    "payment_id": payment_id,
                    "transaction_id": data.get("transactionID")
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"bKash payment creation failed: {response.status_code}"
                )
    
    @staticmethod
    async def execute_payment(payment_id: str, transaction_id: str, db: Session) -> dict:
        """Execute bKash payment after user completes payment"""
        token = await BkashService.get_token()
        
        url = f"{BKASH_BASE_URL}/tokenized/checkout/execute"
        
        payload = {
            "paymentID": payment_id
        }
        
        headers = {
            "Authorization": token,
            "X-App-Key": BKASH_APP_KEY,
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                # Update payment record
                payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
                if payment:
                    payment.status = "completed" if data.get("transactionStatus") == "Completed" else "failed"
                    payment.transaction_id = data.get("transactionID")
                    db.commit()
                
                return {
                    "success": True,
                    "transaction_id": data.get("transactionID"),
                    "status": data.get("transactionStatus"),
                    "amount": data.get("amount")
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"bKash payment execution failed: {response.status_code}"
                )
    
    @staticmethod
    async def query_payment(transaction_id: str) -> dict:
        """Query bKash payment status"""
        token = await BkashService.get_token()
        
        url = f"{BKASH_BASE_URL}/tokenized/checkout/query"
        
        payload = {
            "paymentID": transaction_id
        }
        
        headers = {
            "Authorization": token,
            "X-App-Key": BKASH_APP_KEY,
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "status": data.get("transactionStatus"),
                    "amount": data.get("amount")
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"bKash query failed: {response.status_code}"
                )


# ============================================
# 🔧 NAGAD SERVICE
# ============================================
class NagadService:
    """Nagad Payment Gateway Service"""
    
    @staticmethod
    async def create_payment(tenant_id: str, amount: float, description: str, db: Session) -> dict:
        """Create Nagad payment"""
        # Generate unique order ID
        order_id = f"NAG{uuid.uuid4().hex[:12].upper()}"
        
        # Get tenant details
        tenant = db.query(Tenant).filter(Tenant.tenant_id == tenant_id).first()
        if not tenant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tenant not found"
            )
        
        # Nagad API endpoint
        url = f"{NAGAD_BASE_URL}/api/order/create"
        
        payload = {
            "orderId": order_id,
            "merchantId": NAGAD_MERCHANT_ID,
            "amount": amount,
            "currency": "BDT",
            "description": description,
            "callbackUrl": f"https://your-api-url.com/api/payment/nagad/callback/{order_id}"
        }
        
        headers = {
            "X-API-Key": NAGAD_API_KEY,
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(url, json=payload, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                
                # Store payment record
                payment = Payment(
                    tenant_id=tenant_id,
                    amount=amount,
                    payment_method="nagad",
                    payment_id=order_id,
                    transaction_id=order_id,
                    status="pending",
                    payment_date=datetime.utcnow()
                )
                db.add(payment)
                db.commit()
                
                return {
                    "success": True,
                    "payment_url": data.get("paymentUrl"),
                    "payment_id": order_id,
                    "transaction_id": order_id
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Nagad payment creation failed: {response.status_code}"
                )
    
    @staticmethod
    async def verify_payment(order_id: str) -> dict:
        """Verify Nagad payment"""
        url = f"{NAGAD_BASE_URL}/api/order/verify/{order_id}"
        
        headers = {
            "X-API-Key": NAGAD_API_KEY,
            "Content-Type": "application/json"
        }
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "status": data.get("status"),
                    "amount": data.get("amount")
                }
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Nagad verification failed: {response.status_code}"
                )


# ============================================
# 🚀 PAYMENT API ENDPOINTS
# ============================================

@router.post("/payment/create", response_model=PaymentResponse)
async def create_payment(request: PaymentCreateRequest, db: Session = Depends(get_db)):
    """
    Create payment (bKash or Nagad)
    Returns payment URL for WebView redirect
    """
    try:
        if request.payment_method.lower() == "bkash":
            result = await BkashService.create_payment(
                tenant_id=request.tenant_id,
                amount=request.amount,
                description=request.description,
                db=db
            )
        elif request.payment_method.lower() == "nagad":
            result = await NagadService.create_payment(
                tenant_id=request.tenant_id,
                amount=request.amount,
                description=request.description,
                db=db
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported payment method. Use 'bkash' or 'nagad'"
            )
        
        return PaymentResponse(
            success=True,
            message=f"{request.payment_method} payment created",
            payment_url=result["payment_url"],
            payment_id=result["payment_id"],
            transaction_id=result["transaction_id"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Payment creation failed: {str(e)}"
        )

@router.post("/payment/execute")
async def execute_payment(request: PaymentExecuteRequest, db: Session = Depends(get_db)):
    """
    Execute payment after user completes in WebView
    """
    try:
        # Try bKash first
        try:
            result = await BkashService.execute_payment(
                payment_id=request.payment_id,
                transaction_id=request.transaction_id,
                db=db
            )
            
            return {
                "success": True,
                "message": "Payment completed successfully",
                "transaction_id": result["transaction_id"],
                "status": result["status"]
            }
        except Exception:
            # If not bKash, try Nagad
            result = await NagadService.verify_payment(request.transaction_id)
            
            return {
                "success": True,
                "message": "Payment verified successfully",
                "transaction_id": request.transaction_id,
                "status": result["status"]
            }
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Payment execution failed: {str(e)}"
        )

@router.get("/payment/status/{payment_id}")
async def get_payment_status(payment_id: str, db: Session = Depends(get_db)):
    """Get payment status"""
    payment = db.query(Payment).filter(Payment.payment_id == payment_id).first()
    
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found"
        )
    
    return {
        "payment_id": payment.payment_id,
        "tenant_id": payment.tenant_id,
        "amount": payment.amount,
        "status": payment.status,
        "payment_method": payment.payment_method,
        "payment_date": payment.payment_date.isoformat() if payment.payment_date else None
    }

@router.get("/payments/tenant/{tenant_id}")
async def get_tenant_payments(tenant_id: str, db: Session = Depends(get_db)):
    """Get all payments for a tenant"""
    payments = db.query(Payment).filter(Payment.tenant_id == tenant_id).all()
    
    return [
        {
            "payment_id": p.payment_id,
            "amount": p.amount,
            "status": p.status,
            "payment_method": p.payment_method,
            "payment_date": p.payment_date.isoformat() if p.payment_date else None
        }
        for p in payments
    ]
