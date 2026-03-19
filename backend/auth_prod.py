"""
LIFEASY V30 PRO - Production Authentication with Bcrypt
Secure password hashing for production deployment
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database_prod import get_db
from models import Tenant
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
import os

router = APIRouter()

# Production security settings
SECRET_KEY = os.getenv("JWT_SECRET", "lifeasy_production_secret_key_2026_change_in_prod")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("TOKEN_EXPIRY", "30"))

# Bcrypt password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash password using bcrypt"""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception:
        return False


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


@router.post("/login")
def login(data: dict, db: Session = Depends(get_db)):
    """
    Production login endpoint with bcrypt authentication
    """
    # Get user from database
    user = db.query(Tenant).filter(Tenant.tenant_id == data["tenant_id"]).first()
    
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid tenant ID or password"
        )
    
    # Verify password with bcrypt
    if not verify_password(data["password"], user.password):
        raise HTTPException(
            status_code=401,
            detail="Invalid tenant ID or password"
        )
    
    # Create JWT token
    access_token = create_access_token(
        data={"sub": user.tenant_id}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "tenant_id": user.tenant_id,
        "expires_in": ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }


@router.post("/refresh-token")
def refresh_token(token: str):
    """Refresh expired token"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        tenant_id: str = payload.get("sub")
        
        if tenant_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        new_token = create_access_token(data={"sub": tenant_id})
        
        return {
            "access_token": new_token,
            "token_type": "bearer"
        }
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
