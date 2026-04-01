"""
LIFEASY V30 PRO - Rate Limiter
Prevents spam and abuse by limiting request frequency
"""
import time
from collections import defaultdict


class RateLimiter:
    """Token bucket rate limiter for API requests"""
    
    def __init__(self):
        # Timestamps of recent requests per user
        self.timestamps = defaultdict(list)
        # Maximum requests allowed in window
        self.MAX_REQUESTS = 15
        # Time window in seconds
        self.WINDOW = 10

    def allow(self, user_id):
        """
        Check if request should be allowed for user
        Returns True if within rate limit, False if exceeded
        """
        now = time.time()
        
        # Remove old timestamps outside the window
        self.timestamps[user_id] = [
            t for t in self.timestamps[user_id] 
            if now - t < self.WINDOW
        ]
        
        # Check if limit exceeded
        if len(self.timestamps[user_id]) >= self.MAX_REQUESTS:
            print(f"⚠️  Rate limit exceeded for user {user_id}")
            return False
        
        # Record this request
        self.timestamps[user_id].append(now)
        return True

    def get_remaining(self, user_id):
        """Get remaining requests allowed in current window"""
        now = time.time()
        valid_timestamps = [
            t for t in self.timestamps[user_id] 
            if now - t < self.WINDOW
        ]
        return max(0, self.MAX_REQUESTS - len(valid_timestamps))


# Global rate limiter instance
rate_limiter = RateLimiter()
