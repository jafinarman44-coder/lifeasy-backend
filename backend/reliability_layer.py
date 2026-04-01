"""
LIFEASY V27+ PHASE 6 STEP 11 - Backend Reliability Layer
NON-DESTRUCTIVE: Adds stability without changing business logic
"""
import asyncio
import time
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from collections import deque


class ReliabilityLayer:
    """
    Production-grade reliability enhancements
    All features are ADDITIVE - don't replace existing logic
    """
    
    def __init__(self):
        # Message buffer queue (for offline users)
        self.message_queue: Dict[int, deque] = {}  # {user_id: [messages]}
        self.MAX_QUEUE_SIZE = 100
        
        # Call signal queue
        self.call_signal_queue: Dict[int, deque] = {}
        
        # Rate limiting (anti-spam)
        self.rate_limit_windows: Dict[int, List[float]] = {}
        self.RATE_LIMIT_MAX_REQUESTS = 15
        self.RATE_LIMIT_WINDOW_SECONDS = 10
        
        # Connection tracking
        self.connection_timestamps: Dict[int, float] = {}
        self.last_activity: Dict[int, float] = {}
        
        print("🛡️ Backend Reliability Layer initialized")
    
    # ==================== MESSAGE BUFFER QUEUE ====================
    
    def queue_message(self, user_id: int, message: dict):
        """Queue message for offline user (non-destructive)"""
        if user_id not in self.message_queue:
            self.message_queue[user_id] = deque(maxlen=self.MAX_QUEUE_SIZE)
        
        self.message_queue[user_id].append({
            "message": message,
            "queued_at": time.time()
        })
        
        print(f"💾 Queued message for user {user_id} (queue size: {len(self.message_queue[user_id])})")
    
    def dequeue_messages(self, user_id: int) -> List[dict]:
        """Get and clear queued messages for user (call when user reconnects)"""
        if user_id not in self.message_queue:
            return []
        
        messages = list(self.message_queue[user_id])
        self.message_queue[user_id].clear()
        
        print(f"📤 Delivered {len(messages)} queued messages to user {user_id}")
        return messages
    
    def has_queued_messages(self, user_id: int) -> bool:
        """Check if user has pending messages"""
        return user_id in self.message_queue and len(self.message_queue[user_id]) > 0
    
    # ==================== CALL SIGNAL QUEUE ====================
    
    def queue_call_signal(self, user_id: int, signal: dict):
        """Queue call signaling message for offline user"""
        if user_id not in self.call_signal_queue:
            self.call_signal_queue[user_id] = deque(maxlen=50)
        
        self.call_signal_queue[user_id].append({
            "signal": signal,
            "queued_at": time.time()
        })
        
        print(f"📞 Queued call signal for user {user_id}")
    
    def dequeue_call_signals(self, user_id: int) -> List[dict]:
        """Get and clear queued call signals"""
        if user_id not in self.call_signal_queue:
            return []
        
        signals = [item["signal"] for item in self.call_signal_queue[user_id]]
        self.call_signal_queue[user_id].clear()
        
        print(f"📞 Delivered {len(signals)} queued call signals to user {user_id}")
        return signals
    
    # ==================== RATE LIMITING (ANTI-SPAM) ====================
    
    def check_rate_limit(self, user_id: int) -> bool:
        """
        Check if request is within rate limit
        Returns True if allowed, False if should be rejected
        NON-DESTRUCTIVE: Use alongside existing validation
        """
        now = time.time()
        window_start = now - self.RATE_LIMIT_WINDOW_SECONDS
        
        # Initialize or clean old timestamps
        if user_id not in self.rate_limit_windows:
            self.rate_limit_windows[user_id] = []
        
        # Remove timestamps outside window
        self.rate_limit_windows[user_id] = [
            ts for ts in self.rate_limit_windows[user_id]
            if ts > window_start
        ]
        
        # Check if over limit
        if len(self.rate_limit_windows[user_id]) >= self.RATE_LIMIT_MAX_REQUESTS:
            print(f"⚠️ Rate limit exceeded for user {user_id}")
            return False
        
        # Record this request
        self.rate_limit_windows[user_id].append(now)
        return True
    
    def get_rate_limit_remaining(self, user_id: int) -> int:
        """Get remaining requests allowed in current window"""
        now = time.time()
        window_start = now - self.RATE_LIMIT_WINDOW_SECONDS
        
        if user_id not in self.rate_limit_windows:
            return self.RATE_LIMIT_MAX_REQUESTS
        
        valid_requests = [
            ts for ts in self.rate_limit_windows[user_id]
            if ts > window_start
        ]
        
        return max(0, self.RATE_LIMIT_MAX_REQUESTS - len(valid_requests))
    
    # ==================== CONNECTION TRACKING ====================
    
    def record_connection(self, user_id: int):
        """Record user connection timestamp"""
        self.connection_timestamps[user_id] = time.time()
        self.last_activity[user_id] = time.time()
        print(f"🔌 Connection recorded for user {user_id}")
    
    def record_activity(self, user_id: int):
        """Record user activity (heartbeat, message, etc.)"""
        self.last_activity[user_id] = time.time()
    
    def get_connection_duration(self, user_id: int) -> float:
        """Get how long user has been connected (in seconds)"""
        if user_id not in self.connection_timestamps:
            return 0.0
        
        return time.time() - self.connection_timestamps[user_id]
    
    def get_inactive_users(self, threshold_seconds: int = 300) -> List[int]:
        """Get list of users inactive for more than threshold"""
        now = time.time()
        inactive = []
        
        for user_id, last_seen in self.last_activity.items():
            if now - last_seen > threshold_seconds:
                inactive.append(user_id)
        
        return inactive
    
    def cleanup_user(self, user_id: int):
        """Clean up all data for disconnected user"""
        self.connection_timestamps.pop(user_id, None)
        self.last_activity.pop(user_id, None)
        self.rate_limit_windows.pop(user_id, None)
        self.message_queue.pop(user_id, None)
        self.call_signal_queue.pop(user_id, None)
        
        print(f"🧹 Cleaned up user {user_id}")
    
    # ==================== TIMESTAMP SYNC ====================
    
    def get_server_timestamp(self) -> str:
        """Get synchronized server timestamp"""
        return datetime.utcnow().isoformat()
    
    def validate_timestamp(self, client_timestamp: str, max_drift_seconds: int = 60) -> bool:
        """Validate client timestamp is within acceptable range"""
        try:
            client_time = datetime.fromisoformat(client_timestamp)
            server_time = datetime.utcnow()
            
            drift = abs((server_time - client_time).total_seconds())
            return drift <= max_drift_seconds
            
        except Exception:
            return False
    
    # ==================== STATUS & MONITORING ====================
    
    def get_stats(self) -> dict:
        """Get reliability layer statistics"""
        return {
            "active_connections": len(self.connection_timestamps),
            "users_with_queued_messages": len([u for u in self.message_queue if self.message_queue[u]]),
            "users_with_queued_calls": len([u for u in self.call_signal_queue if self.call_signal_queue[u]]),
            "rate_limited_users": len([
                u for u in self.rate_limit_windows
                if self.get_rate_limit_remaining(u) == 0
            ])
        }


# Global reliability layer instance
reliability_layer = ReliabilityLayer()
