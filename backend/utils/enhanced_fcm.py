"""
LIFEASY V30 PRO - Enhanced FCM Notification System (Q4)
Full-screen call notifications with deep routing
"""
from pyfcm import FCMNotification
from typing import Optional, Dict
import json


class EnhancedFCMManager:
    """
    Enhanced FCM manager with smart notification routing
    Supports: Call, Message, Announcement notifications
    """
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.push_service = FCMNotification(api_key=api_key) if api_key else None
        
        # Notification templates
        self.notification_templates = {
            "call": {
                "title": "Incoming Call",
                "body": "{caller} is calling...",
                "click_action": "FLUTTER_NOTIFICATION_CLICK",
                "category": "CALL"
            },
            "message": {
                "title": "New Message",
                "body": "{sender}: {message}",
                "click_action": "FLUTTER_NOTIFICATION_CLICK",
                "category": "MESSAGE"
            },
            "announcement": {
                "title": "Important Notice",
                "body": "{message}",
                "click_action": "FLUTTER_NOTIFICATION_CLICK",
                "category": "ANNOUNCEMENT"
            }
        }
    
    async def send_call_notification(
        self,
        device_token: str,
        caller_name: str,
        call_type: str = "voice",
        caller_id: Optional[int] = None,
        receiver_id: Optional[int] = None,
        is_video: bool = False
    ):
        """
        Send full-screen call notification
        
        Args:
            device_token: FCM device token
            caller_name: Name of the caller
            call_type: "voice" or "video"
            caller_id: Caller's user ID
            receiver_id: Receiver's user ID
            is_video: True for video call
        """
        if not self.push_service:
            print("⚠️ FCM not configured, skipping call notification")
            return
        
        # High priority for call notifications
        data_message = {
            "type": "incoming_call",
            "caller_name": caller_name,
            "call_type": call_type,
            "caller_id": str(caller_id) if caller_id else "",
            "receiver_id": str(receiver_id) if receiver_id else "",
            "is_video": str(is_video),
            "timestamp": str(int(json.dumps({"time": "now"}))),
            "route": "call_screen",  # Deep link route
            "app_name": "LIFEASY BUILDING APP"
        }
        
        title = f"Incoming {call_type.capitalize()} Call"
        body = f"{caller_name} is calling..."
        
        try:
            result = await self._send_notification(
                registration_id=device_token,
                message_title=title,
                message_body=body,
                data_message=data_message,
                sound="ringtone.wav",  # Custom ringtone
                priority="high",
                content_available=True  # Wake up app
            )
            
            print(f"📱 Call notification sent to {caller_name}")
            return result
            
        except Exception as e:
            print(f"❌ Failed to send call notification: {e}")
            return None
    
    async def send_message_notification(
        self,
        device_token: str,
        sender_name: str,
        message: str,
        sender_id: Optional[int] = None,
        message_id: Optional[int] = None
    ):
        """Send message notification with preview"""
        if not self.push_service:
            return
        
        data_message = {
            "type": "new_message",
            "sender_name": sender_name,
            "sender_id": str(sender_id) if sender_id else "",
            "message_id": str(message_id) if message_id else "",
            "route": "chat_screen",  # Deep link to chat
            "app_name": "LIFEASY BUILDING APP"
        }
        
        # Truncate long messages
        preview = message[:50] + "..." if len(message) > 50 else message
        
        try:
            result = await self._send_notification(
                registration_id=device_token,
                message_title=f"💬 {sender_name}",
                message_body=preview,
                data_message=data_message,
                sound="notification.wav",
                priority="high"
            )
            
            print(f"📧 Message notification sent from {sender_name}")
            return result
            
        except Exception as e:
            print(f"❌ Failed to send message notification: {e}")
            return None
    
    async def send_announcement_notification(
        self,
        device_token: str,
        title: str,
        message: str,
        announcement_id: Optional[int] = None,
        building_id: Optional[str] = None
    ):
        """Send owner/management announcement"""
        if not self.push_service:
            return
        
        data_message = {
            "type": "announcement",
            "title": title,
            "announcement_id": str(announcement_id) if announcement_id else "",
            "building_id": building_id or "",
            "route": "announcement_screen",
            "app_name": "LIFEASY BUILDING APP"
        }
        
        try:
            result = await self._send_notification(
                registration_id=device_token,
                message_title=f"📢 {title}",
                message_body=message,
                data_message=data_message,
                sound="notification.wav",
                priority="high"
            )
            
            print(f"📢 Announcement notification sent: {title}")
            return result
            
        except Exception as e:
            print(f"❌ Failed to send announcement notification: {e}")
            return None
    
    async def _send_notification(
        self,
        registration_id: str,
        message_title: str,
        message_body: str,
        data_message: dict,
        sound: str = "default",
        priority: str = "normal",
        content_available: bool = False
    ):
        """Internal method to send FCM notification"""
        try:
            result = await self.push_service.notify_single_device(
                registration_id=registration_id,
                message_title=message_title,
                message_body=message_body,
                data_message=data_message,
                sound=sound,
                content_available=content_available,
                priority=priority,
                notification_kwargs={
                    "click_action": "FLUTTER_NOTIFICATION_CLICK"
                }
            )
            return result
        except Exception as e:
            raise e
    
    def set_api_key(self, api_key: str):
        """Update API key"""
        self.api_key = api_key
        self.push_service = FCMNotification(api_key=api_key)


# Factory function to create FCM manager
def create_fcm_manager(api_key: str) -> EnhancedFCMManager:
    """Create FCM manager instance"""
    return EnhancedFCMManager(api_key)
