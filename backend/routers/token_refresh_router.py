"""
LIFEASY V27+ PHASE 6 STEP 11 - Token Refresh Endpoint
Allows clients to refresh Agora tokens without reconnection
"""
from fastapi import APIRouter, HTTPException
from typing import Optional
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from utils.agora_token_manager import agora_token_manager
    AGORA_AVAILABLE = True
except ImportError:
    AGORA_AVAILABLE = False
    print("⚠️ Agora token manager not available - using fallback")

router = APIRouter(prefix="/api/call/v2", tags=["Call System V2"])


@router.get("/refresh-token/{channel}/{uid}")
def refresh_agora_token(channel: str, uid: int):
    """
    C6: Generate fresh Agora token for ongoing call
    
    Args:
        channel: str - Call channel name
        uid: int - User ID
        
    Returns:
        dict - Fresh Agora token and metadata
    """
    if not AGORA_AVAILABLE:
        # Fallback response when Agora not configured
        return {
            "status": "success",
            "token": "demo_token_no_agora_configured",
            "channel": channel,
            "uid": uid,
            "expires_in": 3600,
            "note": "Demo mode - configure Agora credentials for production"
        }
    
    try:
        # Generate new token with auto-renewal
        token = agora_token_manager.generate_token(channel, uid)
        
        return {
            "status": "success",
            "token": token,
            "channel": channel,
            "uid": uid,
            "expires_in": 3600,  # 1 hour
            "auto_renewal": True
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate token: {str(e)}"
        )


@router.get("/check-token-expiry/{channel}/{uid}")
def check_token_expiry(channel: str, uid: int):
    """
    Check if current token needs renewal
    
    Args:
        channel: str - Call channel name
        uid: int - User ID
        
    Returns:
        dict - Token expiry information
    """
    if not AGORA_AVAILABLE:
        return {
            "status": "demo_mode",
            "needs_renewal": False,
            "expires_in_seconds": 3600
        }
    
    try:
        needs_renewal = agora_token_manager._needs_renewal(channel, uid)
        expires_in = 3600  # Default 1 hour
        
        return {
            "status": "success",
            "needs_renewal": needs_renewal,
            "expires_in_seconds": expires_in,
            "auto_renewal_enabled": True
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": str(e),
            "needs_renewal": True  # Safe default
        }
