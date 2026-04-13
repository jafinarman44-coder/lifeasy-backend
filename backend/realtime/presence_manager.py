"""
LIFEASY V27 - Presence Manager
Global user presence tracking system
Tracks: online, offline, in_call, typing
"""
import time
from typing import Dict, Optional
from datetime import datetime
from threading import Lock

class PresenceManager:
    """
    Manages global user presence status
    Thread-safe presence tracking
    """
    
    def __init__(self):
        # user_id -> presence data
        self._presence: Dict[int, dict] = {}
        self._lock = Lock()
        
    def set_status(self, user_id: int, status: str, metadata: dict = None):
        """
        Update user presence status
        status: 'online' | 'offline' | 'in_call' | 'typing' | 'away'
        """
        with self._lock:
            self._presence[user_id] = {
                'status': status,
                'updated_at': time.time(),
                'updated_at_iso': datetime.utcnow().isoformat(),
                'metadata': metadata or {}
            }
            
    def get_status(self, user_id: int) -> Optional[dict]:
        """Get user presence status"""
        with self._lock:
            return self._presence.get(user_id)
    
    def is_online(self, user_id: int) -> bool:
        """Check if user is online"""
        with self._lock:
            presence = self._presence.get(user_id)
            if not presence:
                return False
            return presence['status'] in ['online', 'in_call', 'typing']
    
    def is_in_call(self, user_id: int) -> bool:
        """Check if user is currently in a call"""
        with self._lock:
            presence = self._presence.get(user_id)
            if not presence:
                return False
            return presence['status'] == 'in_call'
    
    def get_all_online_users(self) -> list:
        """Get list of all online users"""
        with self._lock:
            return [
                user_id for user_id, data in self._presence.items()
                if data['status'] in ['online', 'in_call', 'typing']
            ]
    
    def cleanup_stale(self, timeout_seconds: int = 60):
        """Remove stale presence records"""
        current_time = time.time()
        with self._lock:
            stale_users = [
                user_id for user_id, data in self._presence.items()
                if current_time - data['updated_at'] > timeout_seconds
            ]
            for user_id in stale_users:
                del self._presence[user_id]
    
    def mark_typing(self, user_id: int, is_typing: bool):
        """Mark user as typing or stop typing"""
        with self._lock:
            presence = self._presence.get(user_id)
            if presence:
                if is_typing:
                    presence['status'] = 'typing'
                    presence['metadata']['typing_since'] = time.time()
                else:
                    presence['status'] = 'online'
                    presence['metadata'].pop('typing_since', None)
                presence['updated_at'] = time.time()
    
    def mark_in_call(self, user_id: int, call_id: str):
        """Mark user as in a call"""
        self.set_status(user_id, 'in_call', {
            'call_id': call_id,
            'call_started_at': time.time()
        })
    
    def mark_call_ended(self, user_id: int):
        """Mark user as online after call ends"""
        with self._lock:
            presence = self._presence.get(user_id)
            if presence and presence['status'] == 'in_call':
                self.set_status(user_id, 'online')
    
    def get_presence_summary(self) -> dict:
        """Get summary of all presence states"""
        with self._lock:
            summary = {
                'online': 0,
                'offline': 0,
                'in_call': 0,
                'typing': 0,
                'away': 0,
                'total_users': len(self._presence)
            }
            
            for data in self._presence.values():
                status = data['status']
                if status in summary:
                    summary[status] += 1
            
            return summary


# Global instance
presence_manager = PresenceManager()
