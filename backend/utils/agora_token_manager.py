"""
LIFEASY V30 PRO - Agora Token Auto-Renewal System
Prevents call drops by renewing tokens before expiration
"""
import asyncio
import time
from datetime import datetime, timedelta
from typing import Dict, Optional, Callable


class AgoraTokenManager:
    """
    Manages Agora token lifecycle with auto-renewal
    Renews tokens 90 minutes before expiration (IMPORTANT)
    """
    
    def __init__(self):
        # Active token storage
        self.tokens: Dict[int, dict] = {}  # {user_id: {token, expires_at, channel}}
        
        # Renewal callbacks
        self.renewal_callbacks: Dict[int, Callable] = {}
        
        # Renewal threshold (90 minutes before expiry)
        self.RENEWAL_THRESHOLD_MINUTES = 90
        
        # Background renewal task
        self.renewal_task: Optional[asyncio.Task] = None
    
    def start_auto_renewal(self):
        """Start background token renewal checker"""
        if self.renewal_task is None:
            self.renewal_task = asyncio.create_task(self._renewal_checker_loop())
            print("🔄 Agora token auto-renewal started")
    
    def stop_auto_renewal(self):
        """Stop background renewal checker"""
        if self.renewal_task:
            self.renewal_task.cancel()
            self.renewal_task = None
            print("⏹️ Agora token auto-renewal stopped")
    
    async def _renewal_checker_loop(self):
        """Check and renew tokens every minute"""
        while True:
            try:
                await asyncio.sleep(60)  # Check every minute
                
                now = datetime.utcnow()
                
                for user_id, token_data in list(self.tokens.items()):
                    expires_at = token_data.get("expires_at")
                    
                    if not expires_at:
                        continue
                    
                    # Calculate time until expiry
                    time_until_expiry = expires_at - now
                    minutes_until_expiry = time_until_expiry.total_seconds() / 60
                    
                    # Renew if within threshold
                    if minutes_until_expiry <= self.RENEWAL_THRESHOLD_MINUTES:
                        print(f"⚠️ Token for user {user_id} expires in {minutes_until_expiry:.1f} min")
                        await self._trigger_renewal(user_id)
                        
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"❌ Error in renewal checker: {e}")
    
    async def _trigger_renewal(self, user_id: int):
        """Trigger token renewal callback"""
        if user_id in self.renewal_callbacks:
            try:
                callback = self.renewal_callbacks[user_id]
                new_token_data = await callback(user_id)
                
                if new_token_data:
                    self.tokens[user_id].update(new_token_data)
                    print(f"✅ Token renewed for user {user_id}")
            except Exception as e:
                print(f"❌ Failed to renew token for user {user_id}: {e}")
    
    def store_token(
        self,
        user_id: int,
        token: str,
        expires_at: datetime,
        channel: str
    ):
        """Store token with expiration tracking"""
        self.tokens[user_id] = {
            "token": token,
            "expires_at": expires_at,
            "channel": channel,
            "created_at": datetime.utcnow()
        }
        print(f"🔑 Stored Agora token for user {user_id} (expires: {expires_at})")
    
    def get_token(self, user_id: int) -> Optional[str]:
        """Get current token for user"""
        if user_id in self.tokens:
            return self.tokens[user_id].get("token")
        return None
    
    def get_expires_at(self, user_id: int) -> Optional[datetime]:
        """Get token expiration time"""
        if user_id in self.tokens:
            return self.tokens[user_id].get("expires_at")
        return None
    
    def register_renewal_callback(self, user_id: int, callback: Callable):
        """Register callback for token renewal"""
        self.renewal_callbacks[user_id] = callback
        print(f"📝 Registered renewal callback for user {user_id}")
    
    def unregister_renewal_callback(self, user_id: int):
        """Unregister renewal callback"""
        if user_id in self.renewal_callbacks:
            del self.renewal_callbacks[user_id]
    
    def remove_token(self, user_id: int):
        """Remove token (on call end)"""
        if user_id in self.tokens:
            del self.tokens[user_id]
            print(f"🗑️ Removed token for user {user_id}")
        
        self.unregister_renewal_callback(user_id)
    
    def get_stats(self) -> dict:
        """Get token manager statistics"""
        now = datetime.utcnow()
        
        active_tokens = 0
        expiring_soon = 0
        
        for token_data in self.tokens.values():
            expires_at = token_data.get("expires_at")
            if expires_at:
                active_tokens += 1
                minutes_until_expiry = (expires_at - now).total_seconds() / 60
                
                if minutes_until_expiry <= self.RENEWAL_THRESHOLD_MINUTES:
                    expiring_soon += 1
        
        return {
            "active_tokens": active_tokens,
            "expiring_within_90min": expiring_soon,
            "registered_callbacks": len(self.renewal_callbacks)
        }


# Global Agora token manager instance
agora_token_manager = AgoraTokenManager()
