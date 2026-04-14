"""
LIFEASY V27+ PHASE 6 - Notification System API
Send notifications to tenants (individual or broadcast)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database_prod import get_db
from models import Notification, Tenant
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

router = APIRouter(prefix="/api/notifications", tags=["Notifications"])


class SendNotificationRequest(BaseModel):
    tenant_id: Optional[int] = None  # None = broadcast to all
    title: str
    message: str


class NotificationResponse(BaseModel):
    id: int
    tenant_id: Optional[int]
    title: str
    message: str
    is_read: bool
    created_at: datetime


@router.post("/send")
def send_notification(data: SendNotificationRequest, db: Session = Depends(get_db)):
    """
    Send notification to a specific tenant or broadcast to all
    Only owner/admin can send notifications
    """
    tenant_id = data.tenant_id
    title = data.title
    message = data.message
    
    # If tenant_id is provided, verify tenant exists
    if tenant_id:
        tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
        if not tenant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={"status": "error", "message": "Tenant not found"}
            )
    
    # Create notification
    notification = Notification(
        tenant_id=tenant_id,  # NULL for broadcast
        title=title,
        message=message,
        is_read=False
    )
    
    db.add(notification)
    db.commit()
    db.refresh(notification)
    
    return {
        "status": "sent",
        "message": "Notification sent successfully",
        "notification": {
            "id": notification.id,
            "tenant_id": tenant_id,
            "title": title,
            "message": message,
            "created_at": notification.created_at.isoformat()
        }
    }


@router.get("/{tenant_id}")
def get_notifications(tenant_id: int, db: Session = Depends(get_db)):
    """
    Get all notifications for a specific tenant
    Includes both individual and broadcast notifications
    """
    try:
        # Get notifications for this tenant + broadcast notifications (NULL tenant_id)
        notifications = db.query(Notification).filter(
            (Notification.tenant_id == tenant_id) | (Notification.tenant_id == None)
        ).order_by(Notification.created_at.desc()).all()
        
        return {
            "status": "success",
            "count": len(notifications),
            "notifications": [
                {
                    "id": n.id,
                    "tenant_id": n.tenant_id,
                    "title": n.title,
                    "message": n.message,
                    "is_read": n.is_read,
                    "created_at": n.created_at.isoformat() if n.created_at else None,
                    "type": "broadcast" if n.tenant_id is None else "individual"
                }
                for n in notifications
            ]
        }
    except Exception as e:
        print(f"❌ ERROR in get_notifications: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching notifications: {str(e)}"
        )


@router.get("/{tenant_id}/unread")
def get_unread_notifications(tenant_id: int, db: Session = Depends(get_db)):
    """
    Get unread notification count for a tenant
    """
    try:
        unread_count = db.query(Notification).filter(
            ((Notification.tenant_id == tenant_id) | (Notification.tenant_id == None)) &
            (Notification.is_read == False)
        ).count()
        
        return {
            "status": "success",
            "unread_count": unread_count
        }
    except Exception as e:
        print(f"❌ ERROR in get_unread_notifications: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching unread count: {str(e)}"
        )


@router.put("/mark-read/{notification_id}")
def mark_notification_as_read(notification_id: int, db: Session = Depends(get_db)):
    """
    Mark a notification as read
    """
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "error", "message": "Notification not found"}
        )
    
    notification.is_read = True
    db.commit()
    
    return {
        "status": "success",
        "message": "Notification marked as read"
    }


@router.delete("/{notification_id}")
def delete_notification(notification_id: int, db: Session = Depends(get_db)):
    """
    Delete a notification
    """
    notification = db.query(Notification).filter(Notification.id == notification_id).first()
    
    if not notification:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "error", "message": "Notification not found"}
        )
    
    db.delete(notification)
    db.commit()
    
    return {
        "status": "success",
        "message": "Notification deleted successfully"
    }
