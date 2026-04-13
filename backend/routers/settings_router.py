"""
LIFEASY V27 - Settings Router
Complete settings management system
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from database_prod import get_db
from models import Tenant
from pydantic import BaseModel
from typing import Optional
import os

router = APIRouter(prefix="/api/settings", tags=["Settings"])

# Pydantic schemas
class ProfileUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None

class PrivacySettings(BaseModel):
    last_seen: str = "Everyone"  # Everyone, Building Only, Nobody
    profile_photo_visibility: str = "Everyone"
    read_receipts: bool = True

class ChatSettings(BaseModel):
    wallpaper: str = "Default"
    media_download_wifi: str = "Auto"
    media_download_mobile: str = "Photos Only"
    media_download_roaming: str = "Never"
    enter_to_send: bool = True

class NotificationSettings(BaseModel):
    message_notifications: bool = True
    group_notifications: bool = True
    call_notifications: bool = True
    vibration: bool = True
    notification_sound: str = "Default"
    call_ringtone: str = "Default"
    popup_notification: bool = True

@router.get("/tenants", tags=["Admin"])
async def get_all_tenants(db: Session = Depends(get_db)):
    """Get all tenants for admin approval (called from Windows app)"""
    
    tenants = db.query(Tenant).all()
    
    tenant_list = []
    for tenant in tenants:
        tenant_list.append({
            "id": tenant.id,
            "email": tenant.email,
            "name": tenant.name,
            "phone": tenant.phone,
            "flat": tenant.flat,
            "building": tenant.building,
            "is_verified": tenant.is_verified,
            "is_active": tenant.is_active,
            "created_at": tenant.created_at.isoformat() if tenant.created_at else None
        })
    
    return {
        "status": "success",
        "data": tenant_list,
        "count": len(tenant_list)
    }

@router.put("/tenants/approve/{email}", tags=["Admin"])
async def approve_tenant(email: str, db: Session = Depends(get_db)):
    """Approve/activate tenant for mobile app access (called from Windows app)"""
    
    tenant = db.query(Tenant).filter(Tenant.email == email).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    tenant.is_active = True
    tenant.is_verified = True
    db.commit()
    db.refresh(tenant)
    
    return {
        "status": "success",
        "message": f"Tenant {email} approved successfully",
        "data": {
            "email": tenant.email,
            "is_active": tenant.is_active,
            "is_verified": tenant.is_verified
        }
    }

@router.put("/tenants/deactivate/{email}", tags=["Admin"])
async def deactivate_tenant(email: str, db: Session = Depends(get_db)):
    """Deactivate tenant mobile app access (called from Windows app)"""
    
    tenant = db.query(Tenant).filter(Tenant.email == email).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    tenant.is_active = False
    db.commit()
    db.refresh(tenant)
    
    return {
        "status": "success",
        "message": f"Tenant {email} deactivated successfully",
        "data": {
            "email": tenant.email,
            "is_active": tenant.is_active
        }
    }

# In-memory storage (use database in production)
user_settings = {}

@router.get("/load/{tenant_id}")
async def load_settings(tenant_id: int, db: Session = Depends(get_db)):
    """Load all user settings"""
    
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    settings = user_settings.get(tenant_id, {
        "privacy": {
            "last_seen": "Everyone",
            "profile_photo_visibility": "Everyone",
            "read_receipts": True
        },
        "chat": {
            "wallpaper": "Default",
            "media_download_wifi": "Auto",
            "media_download_mobile": "Photos Only",
            "media_download_roaming": "Never",
            "enter_to_send": True
        },
        "notifications": {
            "message_notifications": True,
            "group_notifications": True,
            "call_notifications": True,
            "vibration": True,
            "notification_sound": "Default",
            "call_ringtone": "Default",
            "popup_notification": True
        }
    })
    
    return {
        "success": True,
        "settings": settings,
        "profile": {
            "name": tenant.name,
            "email": tenant.email,
            "phone": tenant.phone,
            "flat": tenant.flat,
            "building": tenant.building
        }
    }

@router.post("/save/{tenant_id}")
async def save_settings(tenant_id: int, settings: dict, db: Session = Depends(get_db)):
    """Save user settings"""
    
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    # Update settings
    if tenant_id not in user_settings:
        user_settings[tenant_id] = {}
    
    user_settings[tenant_id].update(settings)
    
    return {
        "success": True,
        "message": "Settings saved successfully"
    }

@router.get("/profile/{tenant_id}")
async def get_profile(tenant_id: int, db: Session = Depends(get_db)):
    """Get tenant profile for mobile app"""
    
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    return {
        "status": "success",
        "data": {
            "name": tenant.name,
            "email": tenant.email,
            "phone": tenant.phone,
            "flat": tenant.flat,
            "building": tenant.building,
            "avatar_url": tenant.avatar_url if hasattr(tenant, 'avatar_url') else None
        }
    }

@router.put("/profile/{tenant_id}")
async def update_profile_v2(tenant_id: int, profile: ProfileUpdate, db: Session = Depends(get_db)):
    """Update profile information (name, email only - flat/building readonly)"""
    
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    # Only allow name and email updates (flat/building are admin-only)
    if profile.name:
        tenant.name = profile.name
    if profile.email:
        tenant.email = profile.email
    # NOTE: flat and building CANNOT be updated by tenant (admin/manager only)
    
    db.commit()
    db.refresh(tenant)
    
    return {
        "status": "success",
        "message": "Profile updated successfully",
        "data": {
            "name": tenant.name,
            "email": tenant.email,
            "flat": tenant.flat,
            "building": tenant.building
        }
    }

@router.post("/profile/avatar-upload")
async def upload_avatar(
    tenant_id: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload profile avatar and save URL to database"""
    
    # Get tenant_id from form data
    tenant_id_int = int(tenant_id)
    
    tenant = db.query(Tenant).filter(Tenant.id == tenant_id_int).first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    
    # Create uploads directory
    upload_dir = f"uploads/avatars/{tenant_id_int}"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate unique filename
    import time
    file_extension = file.filename.split('.')[-1] if file.filename and '.' in file.filename else 'jpg'
    unique_filename = f"avatar_{int(time.time())}.{file_extension}"
    file_path = f"{upload_dir}/{unique_filename}"
    
    # Save file
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Create relative URL path
    avatar_url = f"/uploads/avatars/{tenant_id_int}/{unique_filename}"
    
    # Save to database (add avatar_url column if not exists)
    if not hasattr(tenant, 'avatar_url'):
        # Add column dynamically (one-time migration)
        from sqlalchemy import text
        try:
            db.execute(text(f"ALTER TABLE tenants ADD COLUMN avatar_url TEXT"))
            db.commit()
        except:
            pass  # Column already exists
    
    tenant.avatar_url = avatar_url
    db.commit()
    db.refresh(tenant)
    
    return {
        "status": "success",
        "message": "Avatar uploaded successfully",
        "avatar_url": avatar_url,
        "full_url": f"http://192.168.0.181:8000{avatar_url}"
    }

@router.post("/privacy/update/{tenant_id}")
async def update_privacy(tenant_id: int, privacy: PrivacySettings):
    """Update privacy settings"""
    
    if tenant_id not in user_settings:
        user_settings[tenant_id] = {}
    
    user_settings[tenant_id]["privacy"] = privacy.dict()
    
    return {
        "success": True,
        "message": "Privacy settings updated"
    }

@router.post("/chat/update/{tenant_id}")
async def update_chat_settings(tenant_id: int, chat: ChatSettings):
    """Update chat settings"""
    
    if tenant_id not in user_settings:
        user_settings[tenant_id] = {}
    
    user_settings[tenant_id]["chat"] = chat.dict()
    
    return {
        "success": True,
        "message": "Chat settings updated"
    }

@router.post("/notifications/update/{tenant_id}")
async def update_notification_settings(tenant_id: int, notifications: NotificationSettings):
    """Update notification settings"""
    
    if tenant_id not in user_settings:
        user_settings[tenant_id] = {}
    
    user_settings[tenant_id]["notifications"] = notifications.dict()
    
    return {
        "success": True,
        "message": "Notification settings updated"
    }

@router.get("/blocked/list/{tenant_id}")
async def get_blocked_users(tenant_id: int, db: Session = Depends(get_db)):
    """Get list of blocked users"""
    from models import BlockedUser
    
    blocks = db.query(BlockedUser).filter(BlockedUser.blocker_id == tenant_id).all()
    
    return {
        "success": True,
        "blocked_users": [
            {
                "blocked_id": block.blocked_id,
                "blocked_at": block.blocked_at.isoformat()
            }
            for block in blocks
        ]
    }
