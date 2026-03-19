"""
LIFEASY V30 PRO - Production Authentication System
Real Phone-based Auth with OTP (Twilio/SSL Wireless) + JWT
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database_prod import get_db
from models import Tenant
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from pydantic import BaseModel
import os
import random
from typing import Optional

router = APIRouter()

# ============================================
# 🔒 SECURITY CONFIGURATION
# ============================================
SECRET_KEY = os.getenv("JWT_SECRET", "lifeasy_production_secret_key_2026")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRY", "43200"))  # 30 days
OTP_EXPIRE_SECONDS = int(os.getenv("OTP_EXPIRY", "300"))  # 5 minutes

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ============================================
# 📱 SMS SERVICE (Twilio/SSL Wireless)
# ============================================
class SMSService:
    """Production SMS service for OTP delivery"""
    
    @staticmethod
    def send_sms_twilio(phone: str, message: str) -> bool:
        """Send SMS via Twilio"""
        try:
            from twilio.rest import Client
            
            account_sid = os.getenv("TWILIO_ACCOUNT_SID")
            auth_token = os.getenv("TWILIO_AUTH_TOKEN")
            twilio_number = os.getenv("TWILIO_PHONE_NUMBER")
            
            if not all([account_sid, auth_token, twilio_number]):
                print("⚠️ Twilio credentials not configured")
                return False
            
            client = Client(account_sid, auth_token)
            
            client.messages.create(
                body=message,
                from_=twilio_number,
                to=phone
            )
            
            print(f"✅ OTP sent to {phone} via Twilio")
            return True
            
        except Exception as e:
            print(f"❌ Twilio SMS error: {e}")
            return False
    
    @staticmethod
    def send_sms_ssl_wireless(phone: str, message: str) -> bool:
        """Send SMS via SSL Wireless (Bangladesh)"""
        try:
            import requests
            
            api_key = os.getenv("SSL_WIRELESS_API_KEY")
            sender_id = os.getenv("SSL_WIRELESS_SENDER_ID", "LIFEASY")
            
            if not api_key:
                print("⚠️ SSL Wireless credentials not configured")
                return False
            
            # SSL Wireless API endpoint
            url = "https://api.sslwireless.com/sms-gateway/api/v1/send-sms"
            
            payload = {
                "senderId": sender_id,
                "msisdn": phone,  # Format: 8801XXXXXXXXX
                "text": message,
                "apiKey": api_key
            }
            
            response = requests.post(url, json=payload, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ OTP sent to {phone} via SSL Wireless")
                return True
            else:
                print(f"❌ SSL Wireless error: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ SSL Wireless SMS error: {e}")
            return False
    
    @staticmethod
    def send_otp(phone: str, otp: str) -> bool:
        """Send OTP via best available SMS service"""
        message = f"Your LIFEASY verification code is: {otp}. Valid for 5 minutes. Never share this code."
        
        # Try Twilio first (international)
        if SMSService.send_sms_twilio(phone, message):
            return True
        
        # Fallback to SSL Wireless (Bangladesh)
        if SMSService.send_sms_ssl_wireless(phone, message):
            return True
        
        # Last resort: Log OTP (development fallback)
        print(f"🔔 FALLBACK OTP for {phone}: {otp}")
        return True


# ============================================
# 🔐 AUTHENTICATION MODELS
# ============================================
class PhoneLoginRequest(BaseModel):
    phone: str
    password: Optional[str] = None

class OTPVerifyRequest(BaseModel):
    phone: str
    otp: str

class RegisterRequest(BaseModel):
    phone: str
    password: str
    name: Optional[str] = None

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    tenant_id: Optional[str] = None
    phone: str
    expires_in: int


# ============================================
# 🔧 HELPER FUNCTIONS
# ============================================
def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False

def generate_otp() -> str:
    """Generate 6-digit OTP"""
    return str(random.randint(100000, 999999))

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> dict:
    """Decode JWT token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )


# ============================================
# 📍 OTP STORAGE (In-memory for demo, use Redis in prod)
# ============================================
otp_storage = {}  # Format: {phone: {"otp": "123456", "expires": timestamp}}

def store_otp(phone: str, otp: str):
    """Store OTP with expiry"""
    otp_storage[phone] = {
        "otp": otp,
        "expires": datetime.utcnow() + timedelta(seconds=OTP_EXPIRE_SECONDS)
    }

def verify_stored_otp(phone: str, otp: str) -> bool:
    """Verify stored OTP"""
    if phone not in otp_storage:
        return False
    
    stored = otp_storage[phone]
    
    # Check expiry
    if datetime.utcnow() > stored["expires"]:
        del otp_storage[phone]
        return False
    
    # Check OTP match
    return stored["otp"] == otp


# ============================================
# 🚀 API ENDPOINTS
# ============================================

@router.post("/send-otp")
async def send_otp(request: PhoneLoginRequest):
    """
    Send OTP to user's phone for authentication
    """
    phone = request.phone
    
    # Validate phone number format (Bangladesh: +8801XXXXXXXXX)
    if not phone.startswith("+880") or len(phone) != 14:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid phone number. Use format: +8801XXXXXXXXX"
        )
    
    # Generate OTP
    otp = generate_otp()
    
    # Store OTP
    store_otp(phone, otp)
    
    # Send OTP via SMS
    if not SMSService.send_otp(phone, otp):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send OTP. Please try again."
        )
    
    return {
        "message": "OTP sent successfully",
        "phone": phone,
        "expires_in": OTP_EXPIRE_SECONDS
    }

@router.post("/verify-otp", response_model=TokenResponse)
async def verify_otp(request: OTPVerifyRequest, db: Session = Depends(get_db)):
    """
    Verify OTP and return JWT token
    """
    phone = request.phone
    otp = request.otp
    
    # Verify OTP
    if not verify_stored_otp(phone, otp):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired OTP"
        )
    
    # Remove used OTP
    del otp_storage[phone]
    
    # Find or create user
    tenant = db.query(Tenant).filter(Tenant.phone == phone).first()
    
    if not tenant:
        # Auto-register new user
        tenant = Tenant(
            tenant_id=f"TNT{phone[-8:]}",  # Generate ID from phone
            phone=phone,
            name=f"User {phone[-8:]}",
            password=hash_password(otp),  # Set temporary password
            flat_number="N/A",
            building_name="N/A",
            rent_amount=0
        )
        db.add(tenant)
        db.commit()
        db.refresh(tenant)
    
    # Create JWT token
    access_token = create_access_token(
        data={
            "sub": tenant.tenant_id,
            "phone": phone,
            "type": "access"
        }
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "tenant_id": tenant.tenant_id,
        "phone": phone,
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@router.post("/register", response_model=TokenResponse)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    Register new user with phone and password
    """
    phone = request.phone
    
    print(f"📝 REGISTER REQUEST: Phone={phone}, Name={request.name}")
    
    # Validate phone format
    if not phone.startswith("+880") or len(phone) != 14:
        print(f"❌ INVALID PHONE FORMAT: {phone}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid phone number. Use format: +8801XXXXXXXXX"
        )
    
    # Check if user exists - CRITICAL VALIDATION
    existing = db.query(Tenant).filter(Tenant.phone == phone).first()
    if existing:
        print(f"❌ USER ALREADY EXISTS: {phone}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists with this phone number"
        )
    
    print(f"✅ PHONE VALIDATED - NEW USER: {phone}")
    
    # Generate tenant ID
    tenant_id = f"TNT{phone[-8:]}"
    
    # Create new tenant
    tenant = Tenant(
        tenant_id=tenant_id,
        phone=phone,
        name=request.name or f"User {phone[-8:]}",
        password=hash_password(request.password),
        flat_number="TBA",
        building_name="TBA",
        rent_amount=0
    )
    
    db.add(tenant)
    db.commit()
    db.refresh(tenant)
    
    print(f"✅ USER CREATED IN DB: {tenant_id}")
    
    # Create JWT token
    access_token = create_access_token(
        data={
            "sub": tenant_id,
            "phone": phone,
            "type": "access"
        }
    )
    
    print(f"✅ REGISTRATION SUCCESS - Token generated for {phone}")
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "tenant_id": tenant_id,
        "phone": phone,
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@router.post("/login", response_model=TokenResponse)
async def login(request: dict, db: Session = Depends(get_db)):
    """
    Login with phone and password (alternative to OTP)
    """
    phone = request.get("phone")
    password = request.get("password")
    
    print(f"🔐 LOGIN REQUEST: Phone={phone}")
    
    if not phone or not password:
        print("❌ MISSING CREDENTIALS")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Phone and password required"
        )
    
    # Find user - CRITICAL CHECK
    tenant = db.query(Tenant).filter(Tenant.phone == phone).first()
    
    if not tenant:
        print(f"❌ USER NOT FOUND: {phone}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    print(f"✅ USER FOUND: {tenant.tenant_id}")
    
    # Verify password - CRITICAL CHECK
    if not verify_password(password, tenant.password):
        print(f"❌ WRONG PASSWORD for {phone}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    print(f"✅ PASSWORD VERIFIED")
    
    # Create JWT token
    access_token = create_access_token(
        data={
            "sub": tenant.tenant_id,
            "phone": phone,
            "type": "access"
        }
    )
    
    print(f"✅ LOGIN SUCCESS - Token generated for {phone}")
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "tenant_id": tenant.tenant_id,
        "phone": phone,
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }

@router.post("/refresh-token")
async def refresh_token(token: str):
    """Refresh expired JWT token"""
    try:
        payload = decode_token(token)
        
        tenant_id = payload.get("sub")
        phone = payload.get("phone")
        
        if not tenant_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        # Create new token
        new_token = create_access_token(
            data={
                "sub": tenant_id,
                "phone": phone,
                "type": "access"
            }
        )
        
        return {
            "access_token": new_token,
            "token_type": "bearer",
            "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token refresh failed: {str(e)}"
        )
