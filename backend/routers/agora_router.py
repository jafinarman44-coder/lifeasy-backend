"""
LIFEASY V30 - Agora Token Generator
Real Video/Voice Call Token Generation
"""
from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
import os
import time

try:
    from agora_token_builder import RtcTokenBuilder
    AGORA_AVAILABLE = True
except ImportError:
    AGORA_AVAILABLE = False
    print("⚠️ Agora token builder not installed. Run: pip install agora-token-builder")

router = APIRouter(prefix="/api/agora", tags=["Agora"])

# ============================================
# 🔑 AGORA CONFIGURATION
# ============================================
APP_ID = os.getenv("AGORA_APP_ID", "")
APP_CERTIFICATE = os.getenv("AGORA_APP_CERTIFICATE", "")

# Token expiration time (1 hour)
TOKEN_EXPIRATION = 3600

# ============================================
# 📱 PYDANTIC MODELS
# ============================================
class TokenRequest(BaseModel):
    channel: str
    uid: int
    role: str = "publisher"  # publisher or subscriber

class TokenResponse(BaseModel):
    status: str
    token: str
    channel: str
    uid: int
    expires_in: int

# ============================================
# 🎥 TOKEN GENERATION ENDPOINTS
# ============================================
@router.get("/token/{channel}/{uid}")
async def generate_token(
    channel: str,
    uid: int,
    role: str = Query(default="publisher", description="publisher or subscriber")
):
    """
    Generate Agora RTC token for video/voice calls.
    
    - **channel**: Channel name (usually call session ID)
    - **uid**: User ID (must be unique per user)
    - **role**: publisher (can send/receive) or subscriber (receive only)
    """
    try:
        # Validate configuration
        if not APP_ID or not APP_CERTIFICATE:
            raise HTTPException(
                status_code=500,
                detail="Agora credentials not configured. Check environment variables."
            )
        
        if not AGORA_AVAILABLE:
            raise HTTPException(
                status_code=500,
                detail="Agora token builder not installed. Contact support."
            )
        
        # Set role
        if role == "subscriber":
            role_value = 2  # ROLE_SUBSCRIBER
        else:
            role_value = 1  # ROLE_PUBLISHER
        
        # Calculate expiration
        expiration_time = int(time.time()) + TOKEN_EXPIRATION
        
        # Generate token
        token = RtcTokenBuilder.buildTokenWithUid(
            APP_ID,
            APP_CERTIFICATE,
            channel,
            uid,
            role_value,
            expiration_time
        )
        
        print(f"✅ Agora token generated for channel={channel}, uid={uid}")
        
        return TokenResponse(
            status="success",
            token=token,
            channel=channel,
            uid=uid,
            expires_in=TOKEN_EXPIRATION
        )
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate token: {str(e)}"
        )

@router.get("/token/stream/{channel}/{uid}")
async def generate_stream_token(
    channel: str,
    uid: int
):
    """
    Generate Agora token for live streaming.
    This token has broadcaster role.
    """
    try:
        if not APP_ID or not APP_CERTIFICATE:
            raise HTTPException(
                status_code=500,
                detail="Agora credentials not configured"
            )
        
        expiration_time = int(time.time()) + TOKEN_EXPIRATION
        
        # Token with stream privileges
        token = RtcTokenBuilder.buildTokenWithUid(
            APP_ID,
            APP_CERTIFICATE,
            channel,
            uid,
            1,  # ROLE_PUBLISHER (broadcaster)
            expiration_time
        )
        
        return {
            "status": "success",
            "token": token,
            "channel": channel,
            "uid": uid,
            "role": "broadcaster",
            "expires_in": TOKEN_EXPIRATION
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate stream token: {str(e)}"
        )

@router.get("/status")
async def agora_status():
    """Check Agora configuration status"""
    return {
        "status": "configured" if (APP_ID and APP_CERTIFICATE) else "not_configured",
        "app_id_configured": bool(APP_ID),
        "certificate_configured": bool(APP_CERTIFICATE),
        "sdk_installed": AGORA_AVAILABLE,
        "token_expiration": TOKEN_EXPIRATION
    }
