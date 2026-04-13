"""
LIFEASY V27 - Rate Limiter
Prevents spam and abuse in chat/call systems
"""
import time
from typing import Dict, List
from collections import defaultdict
from threading import Lock

class RateLimiter:
    """
    Advanced rate limiter for chat and call systems
    Tracks message frequency and blocks spam
    """
    
    def __init__(self):
        # Chat rate limiting
        self._chat_history: Dict[int, List[float]] = defaultdict(list)
        
        # Call rate limiting
        self._call_history: Dict[int, List[float]] = defaultdict(list)
        
        self._lock = Lock()
        
        # Rate limits
        self.CHAT_MESSAGES_PER_SECOND = 5
        self.CALL_OFFERS_PER_5_SECONDS = 2
        
    def check_chat_rate(self, user_id: int) -> bool:
        """
        Check if user is sending messages too fast
        Returns True if ALLOWED, False if RATE LIMITED
        """
        current_time = time.time()
        
        with self._lock:
            # Remove timestamps older than 1 second
            self._chat_history[user_id] = [
                ts for ts in self._chat_history[user_id]
                if current_time - ts < 1.0
            ]
            
            # Check if exceeds limit
            if len(self._chat_history[user_id]) >= self.CHAT_MESSAGES_PER_SECOND:
                return False  # Rate limited
            
            # Add current timestamp
            self._chat_history[user_id].append(current_time)
            return True  # Allowed
    
    def check_call_rate(self, user_id: int) -> bool:
        """
        Check if user is making too many call offers
        Returns True if ALLOWED, False if SPAM
        """
        current_time = time.time()
        
        with self._lock:
            # Remove timestamps older than 5 seconds
            self._call_history[user_id] = [
                ts for ts in self._call_history[user_id]
                if current_time - ts < 5.0
            ]
            
            # Check if exceeds limit
            if len(self._call_history[user_id]) >= self.CALL_OFFERS_PER_5_SECONDS:
                return False  # Spam detected
            
            # Add current timestamp
            self._call_history[user_id].append(current_time)
            return True  # Allowed
    
    def get_user_chat_rate(self, user_id: int) -> int:
        """Get current messages per second for user"""
        current_time = time.time()
        
        with self._lock:
            recent = [
                ts for ts in self._chat_history[user_id]
                if current_time - ts < 1.0
            ]
            return len(recent)
    
    def reset_user(self, user_id: int):
        """Reset rate limits for user (e.g., on disconnect)"""
        with self._lock:
            self._chat_history.pop(user_id, None)
            self._call_history.pop(user_id, None)
    
    def cleanup_old_records(self):
        """Remove old rate limit records (run periodically)"""
        current_time = time.time()
        
        with self._lock:
            # Clean chat history
            users_to_remove = []
            for user_id, timestamps in self._chat_history.items():
                self._chat_history[user_id] = [
                    ts for ts in timestamps
                    if current_time - ts < 10.0
                ]
                if not self._chat_history[user_id]:
                    users_to_remove.append(user_id)
            
            for user_id in users_to_remove:
                del self._chat_history[user_id]
            
            # Clean call history
            users_to_remove = []
            for user_id, timestamps in self._call_history.items():
                self._call_history[user_id] = [
                    ts for ts in timestamps
                    if current_time - ts < 30.0
                ]
                if not self._call_history[user_id]:
                    users_to_remove.append(user_id)
            
            for user_id in users_to_remove:
                del self._call_history[user_id]


# Global instance
rate_limiter = RateLimiter()
