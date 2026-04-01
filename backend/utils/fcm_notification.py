"""
LIFEASY V27+ PHASE 6 STEP 7 - Firebase Cloud Messaging (FCM) Push Notifications
Send real-time push notifications for incoming calls and messages
"""
import firebase_admin
from firebase_admin import messaging, credentials
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Firebase Admin SDK
def initialize_firebase():
    """Initialize Firebase Admin SDK with service account"""
    try:
        # Check if already initialized
        if not firebase_admin._apps:
            # Path to your service account key
            cred_path = os.getenv("FIREBASE_CREDENTIALS_PATH", "firebase_service_account.json")
            
            if os.path.exists(cred_path):
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred)
                print("✅ Firebase Admin initialized")
            else:
                print(f"⚠️ Firebase credentials file not found at {cred_path}")
                return False
        return True
    except Exception as e:
        print(f"❌ Firebase initialization error: {e}")
        return False


def send_push_notification(device_token: str, title: str, body: str, 
                          data: dict = None, high_priority: bool = True) -> bool:
    """
    Send push notification to a single device
    
    Args:
        device_token: FCM device token
        title: Notification title
        body: Notification message
        data: Additional data payload
        high_priority: Set high priority for immediate delivery
    
    Returns:
        bool indicating success/failure
    """
    try:
        # Build notification message
        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=device_token,
            android=messaging.AndroidConfig(
                priority='high' if high_priority else 'normal',
                notification=messaging.AndroidNotification(
                    sound='default',
                    click_action='FLUTTER_NOTIFICATION_CLICK',
                )
            ),
            apns=messaging.APNSConfig(
                payload=messaging.APNSPayload(
                    aps=messaging.Aps(
                        sound='default',
                        content_available=True,
                    ),
                ),
            ),
        )
        
        # Add custom data if provided
        if data:
            message.data = data
        
        # Send the message
        response = messaging.send(message)
        print(f"✅ Push notification sent: {response}")
        return True
        
    except messaging.UnregisteredError:
        print(f"❌ Device token not registered")
        return False
    except Exception as e:
        print(f"❌ Error sending push notification: {e}")
        return False


def send_incoming_call_notification(device_token: str, caller_name: str, 
                                   call_type: str = 'voice', 
                                   call_data: dict = None) -> bool:
    """
    Send specialized incoming call notification
    
    Args:
        device_token: Receiver's FCM token
        caller_name: Name of the person calling
        call_type: 'voice' or 'video'
        call_data: Additional call information (caller_id, channel, etc.)
    
    Returns:
        bool indicating success
    """
    try:
        # Build call-specific data
        data = {
            'type': 'incoming_call',
            'caller_name': caller_name,
            'call_type': call_type,
            **(call_data or {})
        }
        
        # Send with high priority for immediate ring
        return send_push_notification(
            device_token=device_token,
            title=f"📞 Incoming {call_type.title()} Call",
            body=f"{caller_name} is calling you...",
            data=data,
            high_priority=True
        )
        
    except Exception as e:
        print(f"❌ Error sending call notification: {e}")
        return False


def send_message_notification(device_token: str, sender_name: str, 
                             message_preview: str,
                             message_data: dict = None) -> bool:
    """
    Send new message notification
    
    Args:
        device_token: Receiver's FCM token
        sender_name: Name of message sender
        message_preview: Preview of message content
        message_data: Additional message info
    
    Returns:
        bool indicating success
    """
    try:
        data = {
            'type': 'new_message',
            'sender_name': sender_name,
            **(message_data or {})
        }
        
        return send_push_notification(
            device_token=device_token,
            title=f"💬 New message from {sender_name}",
            body=message_preview[:100],  # Limit preview length
            data=data,
            high_priority=False
        )
        
    except Exception as e:
        print(f"❌ Error sending message notification: {e}")
        return False


def send_bulk_notifications(device_tokens: list, title: str, body: str,
                           data: dict = None) -> dict:
    """
    Send notifications to multiple devices
    
    Args:
        device_tokens: List of FCM tokens
        title: Notification title
        body: Notification message
        data: Additional data
    
    Returns:
        dict with success/failure counts
    """
    try:
        # Build message for multicast
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            tokens=device_tokens,
            android=messaging.AndroidConfig(
                priority='high',
            ),
            apns=messaging.APNSConfig(
                payload=messaging.APNSPayload(
                    aps=messaging.Aps(
                        sound='default',
                        content_available=True,
                    ),
                ),
            ),
        )
        
        if data:
            message.data = data
        
        # Send to all tokens
        response = messaging.send_multicast(message)
        
        return {
            'success': response.success_count,
            'failure': response.failure_count,
            'total': len(device_tokens)
        }
        
    except Exception as e:
        print(f"❌ Error sending bulk notifications: {e}")
        return {
            'success': 0,
            'failure': len(device_tokens),
            'total': len(device_tokens),
            'error': str(e)
        }


# Initialize on module load
initialize_firebase()
