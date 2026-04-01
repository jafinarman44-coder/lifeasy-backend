"""
LIFEASY V27+ PHASE 6 STEP 11 - Rate Limiting (Anti-Spam) System
Prevents WebSocket message spam and abuse
"""
from collections import defaultdict
import time
from typing import Dict


class RateLimiter:
    """
    Production-grade rate limiter for WebSocket messages
    Features:
    - Per-user rate limiting
    - Configurable time windows
    - Sliding window algorithm
    """
    
    def __init__(self, max_requests: int = 15, window_seconds: float = 10.0):
        """
        Initialize rate limiter
        
        Args:
            max_requests: Maximum requests allowed per window (default: 15)
            window_seconds: Time window in seconds (default: 10)
        """
        # C4: RATE LIMITING TRACKING
        self.request_timestamps: Dict[int, list] = defaultdict(list)
        self.max_requests = max_requests
        self.window_seconds = window_seconds
    
    def is_allowed(self, user_id: int) -> bool:
        """
        Check if request is within rate limit
        
        Args:
            user_id: int - User making the request
            
        Returns:
            bool - True if allowed, False if rate limited
        """
        now = time.time()
        window_start = now - self.window_seconds
        
        # Remove old timestamps outside window
        self.request_timestamps[user_id] = [
            ts for ts in self.request_timestamps[user_id]
            if ts > window_start
        ]
        
        # Check if under limit
        if len(self.request_timestamps[user_id]) >= self.max_requests:
            print(f"⚠️ Rate limit exceeded for user {user_id}")
            return False
        
        # Record this request
        self.request_timestamps[user_id].append(now)
        return True
    
    def check_and_record(self, user_id: int) -> bool:
        """
        Check rate limit and record request if allowed
        
        This is a convenience method that combines checking and recording
        
        Args:
            user_id: int - User making the request
            
        Returns:
            bool - True if allowed, False if rate limited
        """
        if not self.is_allowed(user_id):
            return False
        
        # Already recorded in is_allowed(), but for clarity:
        self.request_timestamps[user_id].append(time.time())
        return True
    
    def get_remaining_requests(self, user_id: int) -> int:
        """Get remaining requests allowed in current window"""
        now = time.time()
        window_start = now - self.window_seconds
        
        valid_requests = [
            ts for ts in self.request_timestamps[user_id]
            if ts > window_start
        ]
        
        return max(0, self.max_requests - len(valid_requests))
    
    def reset_user(self, user_id: int):
        """Reset rate limit tracking for a user"""
        if user_id in self.request_timestamps:
            del self.request_timestamps[user_id]
            print(f"🔄 Reset rate limit for user {user_id}")
    
    def cleanup_old_entries(self):
        """Remove all old entries to free memory"""
        now = time.time()
        window_start = now - self.window_seconds
        
        for user_id in list(self.request_timestamps.keys()):
            self.request_timestamps[user_id] = [
                ts for ts in self.request_timestamps[user_id]
                if ts > window_start
            ]
            
            # Remove empty lists
            if not self.request_timestamps[user_id]:
                del self.request_timestamps[user_id]


# Global rate limiter instance (15 requests per 10 seconds)
rate_limiter = RateLimiter(max_requests=15, window_seconds=10.0)

# ==================== SIMPLE DECORATOR VERSION ====================

def rate_limit_check(user_id: int, min_interval: float = 0.3):
    """
    Simple rate limit decorator for quick implementation
    
    Usage:
        if not rate_limit_check(user_id):
            continue  # Skip this message
    
    Args:
        user_id: int - User ID
        min_interval: float - Minimum seconds between requests (default: 0.3)
        
    Returns:
        bool - True if allowed, False if should skip
    """
    # Track last signal time globally
    global _last_signal_times
    if '_last_signal_times' not in globals():
        _last_signal_times = defaultdict(float)
    
    now = time.time()
    if now - _last_signal_times[user_id] < min_interval:
        return False  # Too soon - skip
    
    _last_signal_times[user_id] = now
    return True
