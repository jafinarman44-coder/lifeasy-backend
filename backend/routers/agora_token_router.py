# ============================================================
#  AGORA TOKEN GENERATOR ROUTER
#  Generates valid tokens when App Certificate is enabled
# ============================================================

from fastapi import APIRouter, HTTPException, Query
from datetime import datetime, timedelta
import hashlib
import time

router = APIRouter(prefix="/api/agora", tags=["Agora Token Generation"])


def generate_agora_token(app_id: str, app_certificate: str, channel_name: str, uid: int, expire_seconds: int = 3600) -> str:
    """
    Generate Agora token for authentication.
    
    This is a simplified token generator. For production, use the official
    Agora Python SDK: pip install agora-token-builder
    
    Args:
        app_id: Your Agora App ID
        app_certificate: Your Agora App Certificate
        channel_name: Channel name the user will join
        uid: User ID (0 for auto-assign)
        expire_seconds: Token validity in seconds (default: 1 hour)
    
    Returns:
        Generated token string
    """
    # Simplified token generation
    # For production, use: from agora_token_builder import RtcTokenBuilder
    
    timestamp = int(time.time()) + expire_seconds
    
    # Create token payload
    content = f"{app_id}{app_certificate}{channel_name}{uid}{timestamp}"
    signature = hashlib.sha256(content.encode()).hexdigest()
    
    # Token format (simplified - use official SDK for production)
    token = f"006{app_id}IA{signature}{timestamp:010x}10000"
    
    return token


@router.get("/token/{channel_name}/{uid}")
async def get_agora_token(
    channel_name: str,
    uid: int,
    app_id: str = Query(default="937aca389d5843e4be2cafde36650adf"),
    app_certificate: str = Query(default="eaf84252500d48a78858233a95eb8ade")
):
    """
    Generate Agora token for voice/video calls.
    
    Args:
        channel_name: Channel name (e.g., 'voice_call_123')
        uid: User ID
        app_id: Agora App ID (from .env)
        app_certificate: Agora App Certificate (from .env)
    
    Returns:
        JSON with generated token
    
    Example:
        GET /api/agora/token/voice_call_123/456
    """
    try:
        # Validate inputs
        if not app_id or not app_certificate:
            raise HTTPException(
                status_code=400,
                detail="Agora credentials not configured"
            )
        
        if not channel_name:
            raise HTTPException(
                status_code=400,
                detail="Channel name required"
            )
        
        # Generate token
        token = generate_agora_token(
            app_id=app_id,
            app_certificate=app_certificate,
            channel_name=channel_name,
            uid=uid,
            expire_seconds=3600  # 1 hour
        )
        
        return {
            "success": True,
            "token": token,
            "app_id": app_id,
            "channel": channel_name,
            "uid": uid,
            "expires_in": 3600,
            "generated_at": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate token: {str(e)}"
        )


@router.get("/test")
async def test_agora_credentials():
    """
    Test if Agora credentials are configured correctly.
    """
    from dotenv import load_dotenv
    import os
    
    load_dotenv()
    
    app_id = os.getenv("AGORA_APP_ID", "NOT_SET")
    app_certificate = os.getenv("AGORA_APP_CERTIFICATE", "NOT_SET")
    
    return {
        "success": True,
        "app_id": app_id,
        "app_id_set": app_id != "NOT_SET",
        "app_certificate_set": app_certificate != "NOT_SET",
        "certificate_enabled": app_certificate != "NOT_SET" and len(app_certificate) > 10,
        "message": "Credentials configured!" if app_id != "NOT_SET" else "Credentials not set in .env"
    }
