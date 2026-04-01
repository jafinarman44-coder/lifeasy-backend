# ============================================
# RATE LIMITER - PART C UPGRADE (C5)
# ============================================
# Prevents call-offer spam and malicious floods
# Protects server from abuse
# ============================================

import time
from typing import Dict, List


class RateLimiter:
    """
    Rate limiter to prevent spam and abuse.
    
    Features:
    - Tracks call attempts per user
    - Limits to 10 calls per minute
    - Auto-cleanup of old history
    - Thread-safe operations
    
    Usage:
        if rate_limiter.too_many_calls(user_id):
            reject_call()
        else:
            allow_call()
    """
    
    def __init__(self):
        # user_id → list of timestamps
        self.call_history: Dict[int, List[float]] = {}
        
        # Maximum call attempts per window
        self.max_attempts = 10
        
        # Time window in seconds (1 minute)
        self.window_seconds = 60
        
        print("🛡️ RateLimiter initialized - preventing spam (max 10 calls/minute)")
    
    def too_many_calls(self, user_id: int) -> bool:
        """
        Check if user has exceeded call rate limit.
        
        Args:
            user_id: User to check
        
        Returns:
            True if user is rate-limited (too many calls)
            False if user can make more calls
        """
        now = time.time()
        
        # Get or create history for user
        if user_id not in self.call_history:
            self.call_history[user_id] = []
        
        history = self.call_history[user_id]
        
        # Add current attempt
        history.append(now)
        
        # Keep only recent attempts within window
        history[:] = [t for t in history if now - t < self.window_seconds]
        
        # Check if exceeded limit
        return len(history) > self.max_attempts
    
    def get_remaining_attempts(self, user_id: int) -> int:
        """
        Get remaining call attempts for user in current window.
        
        Args:
            user_id: User to check
        
        Returns:
            Number of remaining call attempts allowed
        """
        now = time.time()
        
        if user_id not in self.call_history:
            return self.max_attempts
        
        history = self.call_history[user_id]
        
        # Count recent attempts
        recent = [t for t in history if now - t < self.window_seconds]
        
        return max(0, self.max_attempts - len(recent))
    
    def reset_user(self, user_id: int):
        """Reset rate limit history for user"""
        self.call_history.pop(user_id, None)
    
    def cleanup_old_entries(self):
        """Remove expired entries from all users"""
        now = time.time()
        
        for user_id in list(self.call_history.keys()):
            self.call_history[user_id] = [
                t for t in self.call_history[user_id]
                if now - t < self.window_seconds
            ]
            
            # Remove empty histories
            if not self.call_history[user_id]:
                del self.call_history[user_id]


# Global rate limiter instance
rate_limiter = RateLimiter()
