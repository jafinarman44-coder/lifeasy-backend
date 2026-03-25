from fastapi import APIRouter, Depends
from typing import Dict

router = APIRouter(prefix="/api/tenant", tags=["Tenant"])

# 🔥 Dummy কিন্তু production structure (later DB connect হবে)
TENANT_DATA = {
    "1001": {
        "tenant_id": "1001",
        "name": "Jafin Arman",
        "phone": "01700000000",
        "flat": "A1",
        "building": "Lifeasy Tower"
    }
}

@router.get("/home/{tenant_id}")
def tenant_home(tenant_id: str):
    tenant = TENANT_DATA.get(tenant_id)

    if not tenant:
        return {"status": "error", "message": "Tenant not found"}

    return {
        "status": "success",
        "tenant": tenant,
        "summary": {
            "due": 2500,
            "paid": 5000,
            "month": "March"
        }
    }


@router.get("/bills/{tenant_id}")
def tenant_bills(tenant_id: str):
    return {
        "status": "success",
        "bills": [
            {"month": "March", "amount": 3000, "status": "unpaid"},
            {"month": "February", "amount": 3000, "status": "paid"}
        ]
    }


@router.get("/payments/{tenant_id}")
def tenant_payments(tenant_id: str):
    return {
        "status": "success",
        "payments": [
            {"amount": 3000, "method": "bKash", "date": "2026-03-01"}
        ]
    }


@router.get("/profile/{tenant_id}")
def tenant_profile(tenant_id: str):
    return {
        "status": "success",
        "profile": TENANT_DATA.get(tenant_id)
    }
