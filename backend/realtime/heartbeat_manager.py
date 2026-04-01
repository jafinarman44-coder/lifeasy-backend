# ============================================
# LIFEASY – HEARTBEAT MANAGER
# Prevent stale WebSockets & auto-clean clients
# ============================================

import time


class HeartbeatManager:
    """
    Manages WebSocket connection health through heartbeat monitoring
    Features:
    - Tracks last ping timestamp per user
    - Detects stale connections (40 second timeout)
    - Auto-cleanup of dead connections
    """
    
    def __init__(self):
        # user_id → timestamp
        self.last_ping = {}
        # seconds before connection considered dead
        self.timeout = 40
    
    def update(self, user_id: int):
        """Update last heartbeat timestamp for user"""
        self.last_ping[user_id] = time.time()
    
    def is_alive(self, user_id: int) -> bool:
        """Check if user connection is still alive"""
        if user_id not in self.last_ping:
            return False
        return (time.time() - self.last_ping[user_id]) < self.timeout
    
    def cleanup(self):
        """Remove stale users and return list of dead user IDs"""
        dead_users = [
            uid for uid, ts in self.last_ping.items()
            if (time.time() - ts) > self.timeout
        ]
        
        # Remove dead users from tracking
        for uid in dead_users:
            del self.last_ping[uid]
        
        return dead_users


# Global heartbeat manager instance
heartbeat_manager = HeartbeatManager()
