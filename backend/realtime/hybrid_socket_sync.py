"""
LIFEASY V30 PRO - Hybrid Socket Sync Engine
Unified auto-reconnect + cloud sync for Chat & Call sockets
Production-grade reliability with fallback queues
"""
import asyncio
import json
import time
from typing import Dict, List, Optional, Callable
from fastapi import WebSocket
from datetime import datetime


class HybridSocketManager:
    """
    Hybrid Socket Sync Engine (Q1 Option C)
    Combines: Auto-reconnect layer + Cloud sync layer + Fallback queue
    """
    
    def __init__(self):
        # Active connections
        self.connections: Dict[int, WebSocket] = {}
        
        # Connection metadata
        self.connection_meta: Dict[int, dict] = {}  # {user_id: {building_id, last_seen, state}}
        
        # Offline message/call queues
        self.fallback_queue: Dict[int, List[dict]] = {}  # {user_id: [messages]}
        
        # Cloud state storage
        self.cloud_state: Dict[int, dict] = {}  # {user_id: {chat_state, call_state}}
        
        # Reconnect handlers
        self.reconnect_callbacks: Dict[int, Callable] = {}
        
        # Heartbeat settings
        self.HEARTBEAT_INTERVAL = 15  # seconds
        self.HEARTBEAT_TIMEOUT = 30   # seconds
        
    async def connect(
        self,
        user_id: int,
        building_id: int,
        websocket: WebSocket,
        socket_type: str = "chat"  # "chat" or "call"
    ):
        """Connect with auto-recovery and cloud sync"""
        await websocket.accept()
        
        # Store connection
        self.connections[user_id] = websocket
        self.connection_meta[user_id] = {
            "building_id": building_id,
            "socket_type": socket_type,
            "last_seen": time.time(),
            "state": "active",
            "connected_at": datetime.utcnow()
        }
        
        print(f"🔌 Hybrid connect: User {user_id} in Building {building_id} ({socket_type})")
        
        # Restore cloud state if exists
        if user_id in self.cloud_state:
            await self._restore_cloud_state(user_id, websocket)
        
        # Deliver pending fallback messages
        await self._deliver_fallback_messages(user_id)
        
        # Start heartbeat monitor
        asyncio.create_task(self._heartbeat_loop(user_id))
    
    def disconnect(self, user_id: int):
        """Disconnect and save state to cloud"""
        if user_id in self.connections:
            del self.connections[user_id]
        
        # Update state to cloud
        if user_id in self.connection_meta:
            self.connection_meta[user_id]["state"] = "disconnected"
            self.connection_meta[user_id]["disconnected_at"] = datetime.utcnow()
        
        # Save current state to cloud memory
        self._save_cloud_state(user_id)
        
        print(f"🔌 Hybrid disconnect: User {user_id}")
    
    async def send(self, user_id: int, data: dict, reliable: bool = True) -> bool:
        """
        Send message with fallback queue support
        
        Args:
            user_id: Target user
            data: Message data
            reliable: If True, queue for delivery when offline
        
        Returns:
            bool: True if sent successfully
        """
        if user_id not in self.connections:
            if reliable:
                # Queue for later delivery
                self.fallback_queue.setdefault(user_id, []).append({
                    "data": data,
                    "timestamp": time.time(),
                    "type": "message"
                })
                print(f"💾 Queued fallback message for user {user_id}")
            return False
        
        try:
            await self.connections[user_id].send_json(data)
            return True
        except Exception as e:
            print(f"❌ Send failed for user {user_id}: {e}")
            self.disconnect(user_id)
            
            if reliable:
                self.fallback_queue.setdefault(user_id, []).append({
                    "data": data,
                    "timestamp": time.time(),
                    "type": "message"
                })
            return False
    
    async def broadcast_building(
        self,
        building_id: int,
        data: dict,
        exclude: Optional[int] = None
    ):
        """Broadcast to all users in a building with fallback"""
        for uid, meta in list(self.connection_meta.items()):
            if meta.get("building_id") == building_id and uid != exclude:
                await self.send(uid, data, reliable=True)
    
    def _save_cloud_state(self, user_id: int):
        """Save user's current state to cloud memory"""
        if user_id in self.connection_meta:
            self.cloud_state[user_id] = {
                "meta": self.connection_meta[user_id],
                "fallback_count": len(self.fallback_queue.get(user_id, [])),
                "updated_at": datetime.utcnow()
            }
            print(f"☁️ Saved cloud state for user {user_id}")
    
    async def _restore_cloud_state(self, user_id: int, websocket: WebSocket):
        """Restore state from cloud on reconnect"""
        if user_id not in self.cloud_state:
            return
        
        state = self.cloud_state[user_id]
        print(f"♻️ Restoring cloud state for user {user_id}: {state}")
        
        # Notify client about restored state
        try:
            await websocket.send_json({
                "action": "state_restored",
                "state": state
            })
        except Exception as e:
            print(f"Error restoring state: {e}")
    
    async def _deliver_fallback_messages(self, user_id: int):
        """Deliver queued messages on reconnect"""
        if user_id not in self.fallback_queue:
            return
        
        messages = self.fallback_queue.pop(user_id, [])
        print(f"📤 Delivering {len(messages)} fallback messages to user {user_id}")
        
        for msg in messages:
            try:
                if user_id in self.connections:
                    await self.connections[user_id].send_json(msg["data"])
            except Exception as e:
                print(f"Error delivering fallback: {e}")
                # Re-queue if delivery fails
                self.fallback_queue.setdefault(user_id, []).append(msg)
    
    async def _heartbeat_loop(self, user_id: int):
        """Monitor connection health with heartbeat"""
        while user_id in self.connections:
            await asyncio.sleep(self.HEARTBEAT_INTERVAL)
            
            if user_id not in self.connection_meta:
                break
            
            last_seen = self.connection_meta[user_id].get("last_seen", 0)
            if time.time() - last_seen > self.HEARTBEAT_TIMEOUT:
                print(f"⚠️ Heartbeat timeout for user {user_id}")
                self.disconnect(user_id)
                break
    
    def update_last_seen(self, user_id: int):
        """Update last seen timestamp"""
        if user_id in self.connection_meta:
            self.connection_meta[user_id]["last_seen"] = time.time()
    
    def set_call_state(self, user_id: int, call_state: str, partner_id: Optional[int] = None):
        """
        Set user's call state in cloud memory
        
        States: "idle", "in-call", "busy", "ringing"
        """
        if user_id not in self.cloud_state:
            self.cloud_state[user_id] = {}
        
        self.cloud_state[user_id]["call_state"] = {
            "state": call_state,
            "partner_id": partner_id,
            "updated_at": datetime.utcnow()
        }
        print(f"📞 Call state for user {user_id}: {call_state}")
    
    def get_call_state(self, user_id: int) -> Optional[dict]:
        """Get user's current call state from cloud"""
        if user_id in self.cloud_state:
            return self.cloud_state[user_id].get("call_state")
        return None
    
    def is_user_available(self, user_id: int) -> bool:
        """Check if user is available for calls/messages"""
        if user_id not in self.connections:
            return False
        
        call_state = self.get_call_state(user_id)
        if call_state and call_state.get("state") == "in-call":
            return False
        
        return True
    
    def get_stats(self) -> dict:
        """Get hybrid manager statistics"""
        return {
            "active_connections": len(self.connections),
            "cloud_states": len(self.cloud_state),
            "fallback_queues": sum(len(q) for q in self.fallback_queue.values()),
            "users_with_fallback": len(self.fallback_queue)
        }


# Global hybrid socket manager instance
hybrid_socket_manager = HybridSocketManager()
