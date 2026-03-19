from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.payment import Payment

router = APIRouter()

@router.get("/payments/tenant/{tenant_id}")
def get_payments(tenant_id: str, db: Session = Depends(get_db)):
    """Get all payments for a tenant"""
    # Demo data - replace with actual DB query
    return [
        {
            "id": 1,
            "date": "2026-01-10",
            "amount": 5000.0,
            "method": "bKash",
            "receipt_number": "RCP-001"
        },
        {
            "id": 2,
            "date": "2026-02-10",
            "amount": 5000.0,
            "method": "Nagad",
            "receipt_number": "RCP-002"
        }
    ]

@router.post("/payments")
def create_payment(payment_data: dict, db: Session = Depends(get_db)):
    """Create new payment"""
    return {
        "status": "success",
        "message": "Payment created successfully",
        "payment": payment_data
    }
