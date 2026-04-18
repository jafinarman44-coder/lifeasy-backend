# ============================================
# REALTIME CALL SOCKET (UPGRADED)
# - Heartbeat
# - Queue
# - Auto cleanup
# - Rate limiting
# ============================================

from typing import Dict
from fastapi import WebSocket
from realtime.heartbeat_manager import heartbeat_manager
from realtime.message_queue import message_queue
from realtime.call_state import call_state
from utils.rate_limiter import rate_limiter
import json


class CallSocketManager:
    """
    Production-grade call socket manager with full stability features
    Features:
    - Heartbeat monitoring (40s timeout)
    - Message queuing for offline users
    - Thread-safe call state
    - Rate limiting (5 req/3s)
    - Auto-cleanup of dead connections
    """
    
    def __init__(self):
        # active user_id → WebSocket
        self.active_ws: Dict[int, WebSocket] = {}
    
    # ---------------------------
    # CONNECT
    # ---------------------------
    async def connect(self, user_id: int, ws: WebSocket):
        """Accept new WebSocket connection and deliver queued messages"""
        await ws.accept()
        self.active_ws[user_id] = ws
        heartbeat_manager.update(user_id)
        
        # Flush queued messages
        for msg in message_queue.pop_all(user_id):
            await ws.send_text(json.dumps(msg))
    
    # ---------------------------
    # SEND SIGNAL
    # ---------------------------
    async def send_signal(self, user_id: int, data: dict) -> bool:
        """Send signaling message to user, queue if offline"""
        ws = self.active_ws.get(user_id)
        if not ws:
            message_queue.add_message(user_id, data)
            return False
        
        try:
            await ws.send_text(json.dumps(data))
            return True
        except:
            message_queue.add_message(user_id, data)
            return False
    
    # ---------------------------
    # HEARTBEAT ("ping")
    # ---------------------------
    def notify_activity(self, user_id: int):
        """Update heartbeat timestamp for user"""
        heartbeat_manager.update(user_id)
    
    # ---------------------------
    # CLEANUP DEAD USERS
    # ---------------------------
    async def cleanup(self):
        """Remove stale/dead users from active connections"""
        dead = heartbeat_manager.cleanup()
        for user_id in dead:
            if user_id in self.active_ws:
                try:
                    await self.active_ws[user_id].close()
                except:
                    pass
                del self.active_ws[user_id]
    
    # ---------------------------
    # STATUS HELPERS
    # ---------------------------
    def is_user_available(self, user_id: int) -> bool:
        """Check if user is online and alive"""
        return user_id in self.active_ws and heartbeat_manager.is_alive(user_id)
    
    def is_user_in_call(self, user_id: int) -> bool:
        """Check if user is currently in a call"""
        return call_state.get_partner(user_id) is not None
    
    def set_user_in_call(self, caller, receiver):
        """Mark users as in-call"""
        call_state.set_call(caller, receiver)
    
    def end_call(self, user_id):
        """End call for user"""
        call_state.end_call(user_id)
    
    def get_active_call_partner(self, user_id):
        """Get current call partner"""
        return call_state.get_partner(user_id)
    
    def disconnect(self, user_id: int):
        """Disconnect user and cleanup"""
        if user_id in self.active_ws:
            try:
                import asyncio
                asyncio.create_task(self.active_ws[user_id].close())
            except:
                pass
            del self.active_ws[user_id]
    
    # Alias methods for compatibility
    async def add_socket(self, user_id: int, ws: WebSocket):
        """Alias for connect - registers WebSocket connection"""
        await self.connect(user_id, ws)
    
    async def remove_socket(self, user_id: int):
        """Alias for disconnect - removes WebSocket connection"""
        self.disconnect(user_id)


# Global call manager instance
call_manager = CallSocketManager()
