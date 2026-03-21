from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Tenant
from jose import jwt
import hashlib
from datetime import datetime, timedelta

router = APIRouter()

SECRET = "lifeasy_secret_key"
ALGORITHM = "HS256"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain, hashed):
    return hash_password(plain) == hashed

def create_token(data: dict):
    data.update({"exp": datetime.utcnow() + timedelta(minutes=30)})
    return jwt.encode(data, SECRET, algorithm=ALGORITHM)

@router.post("/login")
def login(data: dict, db: Session = Depends(get_db)):
    user = db.query(Tenant).filter(Tenant.tenant_id == data["tenant_id"]).first()

    if not user or not verify_password(data["password"], user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_token({"sub": user.tenant_id})

    return {
        "access_token": token,
        "tenant_id": user.tenant_id
    }

@router.post("/send-otp")
def send_otp():
    return {"msg": "otp sent"}

@router.post("/verify-otp")
def verify():
    return {"msg": "verified"}
