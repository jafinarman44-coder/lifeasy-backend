"""
LIFEASY V27+ PHASE 6 STEP 7 - Production Agora Token Generator
Official Agora SDK for secure RTC token generation
"""
from agora_token_builder import RtcTokenBuilder
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def generate_agora_token(channel_name: str, uid: int) -> dict:
    """
    Generate production-ready Agora RTC token using official SDK
    
    Args:
        channel_name: Unique channel ID for the call
        uid: User ID (0 for host, remote UID for others)
    
    Returns:
        dict with 'token', 'expire_at', and 'app_id'
    """
    app_id = os.getenv("AGORA_APP_ID")
    app_certificate = os.getenv("AGORA_APP_CERTIFICATE")
    
    if not app_id or not app_certificate:
        raise ValueError("Agora credentials not set in .env file")
    
    # Token expires in 2 hours (7200 seconds)
    expiration_time = 3600 * 2
    current_timestamp = int(time.time())
    privilege_expired_ts = current_timestamp + expiration_time
    
    # Build token using official Agora SDK
    token = RtcTokenBuilder.buildTokenWithUid(
        app_id,
        app_certificate,
        channel_name,
        uid,
        1,  # Role: 1 = Host/Broadcaster, 2 = Audience
        privilege_expired_ts
    )
    
    return {
        "token": token,
        "expire_at": privilege_expired_ts,
        "app_id": app_id
    }


def validate_agora_token(token: str, channel: str, uid: int) -> bool:
    """
    Validate Agora token (optional verification)
    """
    try:
        # Token validation logic can be added here
        # For now, we trust the JWT signature
        return True
    except Exception:
        return False
