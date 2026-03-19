from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.tenant import Tenant

router = APIRouter()

@router.get("/tenants/{tenant_id}")
def get_tenant(tenant_id: str, db: Session = Depends(get_db)):
    """Get tenant profile by ID"""
    # Demo data - replace with actual DB query
    return {
        "tenant_id": tenant_id,
        "name": "Demo Tenant",
        "email": "tenant@example.com",
        "phone": "+8801234567890",
        "flat_number": "A-101",
        "unit_number": "Unit-1"
    }

@router.get("/tenants")
def list_tenants(db: Session = Depends(get_db)):
    """List all tenants"""
    return []
