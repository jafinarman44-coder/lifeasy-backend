"""
LIFEASY V30 PRO - Firebase Cloud Messaging Service
Push Notifications for Mobile App
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database_prod import get_db
from models import Tenant
from pydantic import BaseModel
from typing import Optional
import os

router = APIRouter()

# ============================================
# 🔔 FIREBASE CONFIGURATION
# ============================================
FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH", "./firebase_credentials.json")
FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID")


# ============================================
# 🔧 FIREBASE SERVICE
# ============================================
class FirebaseService:
    """Firebase Cloud Messaging Service"""
    
    _initialized = False
    
    @staticmethod
    def initialize():
        """Initialize Firebase Admin SDK"""
        if FirebaseService._initialized:
            return
        
        try:
            import firebase_admin
            from firebase_admin import credentials
            
            # Initialize Firebase
            if os.path.exists(FIREBASE_CREDENTIALS_PATH):
                cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
                firebase_admin.initialize_app(cred, {
                    'projectId': FIREBASE_PROJECT_ID or 'lifeasy'
                })
                FirebaseService._initialized = True
                print(f"✅ Firebase initialized: {FIREBASE_PROJECT_ID}")
            else:
                print(f"⚠️ Firebase credentials not found: {FIREBASE_CREDENTIALS_PATH}")
                
        except Exception as e:
            print(f"❌ Firebase initialization error: {e}")
    
    @staticmethod
    def send_notification(
        device_token: str,
        title: str,
        body: str,
        data: Optional[dict] = None
    ) -> bool:
        """Send push notification to device"""
        try:
            # Auto-initialize if needed
            FirebaseService.initialize()
            
            if not FirebaseService._initialized:
                print("⚠️ Firebase not initialized, skipping notification")
                return False
            
            from firebase_admin import messaging
            
            # Build message
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body,
                ),
                token=device_token,
                data=data,  # Custom data payload
                android=messaging.AndroidConfig(
                    priority='high',
                    notification=messaging.AndroidNotification(
                        sound='default',
                        click_action='OPEN_NOTIFICATION'
                    )
                ),
                apns=messaging.APNSConfig(
                    payload=messaging.APNSPayload(
                        aps=messaging.Aps(
                            sound='default',
                            category='NOTIFICATION_CATEGORY'
                        )
                    )
                )
            )
            
            # Send message
            response = messaging.send(message)
            
            print(f"✅ Notification sent: {title} to {device_token}")
            return True
            
        except Exception as e:
            print(f"❌ Firebase notification error: {e}")
            return False
    
    @staticmethod
    def send_to_topic(
        topic: str,
        title: str,
        body: str,
        data: Optional[dict] = None
    ) -> bool:
        """Send notification to topic (multiple devices)"""
        try:
            FirebaseService.initialize()
            
            if not FirebaseService._initialized:
                return False
            
            from firebase_admin import messaging
            
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body,
                ),
                topic=topic,
                data=data,
                android=messaging.AndroidConfig(
                    priority='high',
                    notification=messaging.AndroidNotification(
                        sound='default'
                    )
                )
            )
            
            response = messaging.send(message)
            
            print(f"✅ Topic notification sent: {title} to {topic}")
            return True
            
        except Exception as e:
            print(f"❌ Firebase topic notification error: {e}")
            return False
    
    @staticmethod
    def send_bulk_notifications(
        device_tokens: list,
        title: str,
        body: str,
        data: Optional[dict] = None
    ) -> dict:
        """Send notifications to multiple devices"""
        try:
            FirebaseService.initialize()
            
            if not FirebaseService._initialized:
                return {"success": 0, "failed": len(device_tokens)}
            
            from firebase_admin import messaging
            
            message = messaging.MulticastMessage(
                notification=messaging.Notification(
                    title=title,
                    body=body,
                ),
                tokens=device_tokens,
                data=data,
                android=messaging.AndroidConfig(
                    priority='high',
                    notification=messaging.AndroidNotification(
                        sound='default'
                    )
                )
            )
            
            response = messaging.send_each_for_multicast(message)
            
            success_count = response.success_count
            failed_count = response.failure_count
            
            print(f"✅ Bulk notifications: {success_count} sent, {failed_count} failed")
            
            return {
                "success": success_count,
                "failed": failed_count,
                "details": response.responses
            }
            
        except Exception as e:
            print(f"❌ Firebase bulk notification error: {e}")
            return {
                "success": 0,
                "failed": len(device_tokens),
                "error": str(e)
            }


# ============================================
# 📱 NOTIFICATION MODELS
# ============================================
class NotificationRequest(BaseModel):
    tenant_id: str
    title: str
    body: str
    type: str = "general"  # general, payment, alert
    data: Optional[dict] = None

class BulkNotificationRequest(BaseModel):
    tenant_ids: list[str]
    title: str
    body: str
    type: str = "general"
    data: Optional[dict] = None


# ============================================
# 🚀 NOTIFICATION ENDPOINTS
# ============================================

@router.post("/notification/send")
async def send_notification(request: NotificationRequest, db: Session = Depends(get_db)):
    """
    Send push notification to a tenant
    """
    # Get tenant
    tenant = db.query(Tenant).filter(Tenant.tenant_id == request.tenant_id).first()
    
    if not tenant:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tenant not found"
        )
    
    # Get device token (in real app, store in database)
    device_token = tenant.device_token if hasattr(tenant, 'device_token') else None
    
    if not device_token:
        return {
            "success": False,
            "message": "Device token not available"
        }
    
    # Send notification
    success = FirebaseService.send_notification(
        device_token=device_token,
        title=request.title,
        body=request.body,
        data={
            "type": request.type,
            "tenant_id": request.tenant_id,
            **(request.data or {})
        }
    )
    
    if success:
        return {
            "success": True,
            "message": "Notification sent successfully"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send notification"
        )

@router.post("/notification/broadcast")
async def broadcast_notification(request: BulkNotificationRequest, db: Session = Depends(get_db)):
    """
    Broadcast notification to multiple tenants
    """
    # Get all target tenants
    tenants = db.query(Tenant).filter(
        Tenant.tenant_id.in_(request.tenant_ids)
    ).all()
    
    if not tenants:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No tenants found"
        )
    
    # Collect device tokens
    device_tokens = []
    for tenant in tenants:
        if hasattr(tenant, 'device_token') and tenant.device_token:
            device_tokens.append(tenant.device_token)
    
    if not device_tokens:
        return {
            "success": False,
            "message": "No device tokens available"
        }
    
    # Send bulk notifications
    result = FirebaseService.send_bulk_notifications(
        device_tokens=device_tokens,
        title=request.title,
        body=request.body,
        data={
            "type": request.type,
            "tenant_ids": ",".join(request.tenant_ids),
            **(request.data or {})
        }
    )
    
    return {
        "success": True,
        "sent": result.get("success", 0),
        "failed": result.get("failed", 0),
        "total": len(device_tokens)
    }

@router.post("/notification/topic/{topic}")
async def send_to_topic(topic: str, title: str, body: str):
    """
    Send notification to topic (all subscribers)
    Useful for announcements
    """
    success = FirebaseService.send_to_topic(
        topic=topic,
        title=title,
        body=body
    )
    
    if success:
        return {
            "success": True,
            "message": f"Notification sent to topic: {topic}"
        }
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send topic notification"
        )


# ============================================
# 🔔 HELPER FUNCTIONS
# ============================================
def send_payment_notification(tenant_id: str, amount: float, status: str):
    """Helper function to send payment notification"""
    title = "Payment Successful! 🎉" if status == "completed" else "Payment Failed ⚠️"
    body = f"Your payment of ৳{amount} has been {status}."
    
    # This would be called from payment gateway after successful transaction
    return {
        "tenant_id": tenant_id,
        "title": title,
        "body": body,
        "type": "payment",
        "data": {
            "amount": str(amount),
            "status": status
        }
    }
