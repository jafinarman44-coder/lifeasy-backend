from fastapi import APIRouter, Depends, HTTPException
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database_prod import get_db

router = APIRouter()

@router.get("/bills/tenant/{tenant_id}")
def get_bills(tenant_id: str, db: Session = Depends(get_db)):
    """Get all bills for a tenant"""
    # Demo data - replace with actual DB query
    return [
        {
            "id": 1,
            "month": "January",
            "year": 2026,
            "amount": 5000.0,
            "status": "unpaid",
            "due_date": "2026-01-10"
        },
        {
            "id": 2,
            "month": "February",
            "year": 2026,
            "amount": 5000.0,
            "status": "paid",
            "due_date": "2026-02-10"
        }
    ]

@router.get("/bills/{bill_id}")
def get_bill(bill_id: int, db: Session = Depends(get_db)):
    """Get specific bill details"""
    return {
        "id": bill_id,
        "month": "January",
        "amount": 5000.0,
        "status": "unpaid"
    }
