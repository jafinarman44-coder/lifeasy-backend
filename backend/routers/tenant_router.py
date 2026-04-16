from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from database_prod import get_db, SessionLocal as ProdSessionLocal
from models import Tenant as TenantProd, ChatPresence
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter()

# Pydantic schema for tenant response
class TenantResponse(BaseModel):
    id: int
    name: str
    email: str
    phone: Optional[str] = None
    flat: Optional[str] = None
    building: Optional[str] = None
    is_active: bool
    is_verified: bool
    online_status: str = 'offline'
    
    class Config:
        from_attributes = True

@router.get("/all", response_model=List[TenantResponse])
def list_all_tenants(
    building_id: int = Query(None, description="Filter by building ID"),
    search: str = Query(None, description="Search by name or email"),
    include_offline: bool = Query(True, description="Include offline tenants")
):
    """
    List all tenants with online status.
    Used for tenant-to-tenant communication.
    """
    try:
        db = ProdSessionLocal()
        
        # Base query
        query = db.query(TenantProd)
        
        # Filter by building if provided
        if building_id:
            query = query.filter(TenantProd.building == building_id)
        
        # Search by name or email
        if search:
            query = query.filter(
                or_(
                    TenantProd.name.ilike(f"%{search}%"),
                    TenantProd.email.ilike(f"%{search}%")
                )
            )
        
        # Get all active tenants
        tenants = query.all()
        
        # Build response with online status
        result = []
        for tenant in tenants:
            # Check online presence
            presence = db.query(ChatPresence).filter(
                ChatPresence.user_id == tenant.id
            ).first()
            
            online_status = 'offline'
            if presence:
                online_status = presence.status
            
            result.append(TenantResponse(
                id=tenant.id,
                name=tenant.name,
                email=tenant.email,
                phone=tenant.phone,
                flat=tenant.flat,
                building=tenant.building,
                is_active=tenant.is_active,
                is_verified=tenant.is_verified,
                online_status=online_status
            ))
        
        db.close()
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing tenants: {str(e)}")

@router.get("/profile/{tenant_id}")
async def get_tenant_profile(tenant_id: int, db: Session = Depends(get_db)):
    """Get REAL tenant profile from database"""
    tenant = db.query(TenantProd).filter(TenantProd.id == tenant_id).first()
    
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    # Check online presence
    presence = db.query(ChatPresence).filter(
        ChatPresence.user_id == tenant_id
    ).first()
    
    online_status = 'offline'
    if presence:
        online_status = presence.status
    
    return {
        "status": "success",
        "data": {
            "id": tenant.id,
            "name": tenant.name,
            "email": tenant.email,
            "phone": tenant.phone,
            "flat": tenant.flat,
            "building": tenant.building,
            "is_active": tenant.is_active,
            "is_verified": tenant.is_verified,
            "online_status": online_status,
            "avatar_url": tenant.avatar_url if hasattr(tenant, 'avatar_url') else None
        }
    }

@router.post("/approve/{tenant_id}")
async def approve_tenant(tenant_id: int):
    """
    Approve a tenant account from mobile app.
    This endpoint activates the tenant account.
    """
    try:
        db = ProdSessionLocal()
        
        # Find tenant
        tenant = db.query(TenantProd).filter(TenantProd.id == tenant_id).first()
        
        if not tenant:
            db.close()
            raise HTTPException(status_code=404, detail="Tenant not found")
        
        # Approve the tenant
        tenant.is_active = True
        tenant.is_verified = True
        db.commit()
        
        db.close()
        
        return {
            "status": "success",
            "message": f"Tenant {tenant.name} has been approved successfully",
            "data": {
                "id": tenant.id,
                "name": tenant.name,
                "email": tenant.email,
                "is_active": tenant.is_active,
                "is_verified": tenant.is_verified
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error approving tenant: {str(e)}")
