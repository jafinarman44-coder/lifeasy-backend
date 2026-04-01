"""
LIFEASY V27+ PHASE 6 STEP 4 - Real-Time Chat WebSocket Server
Handles real-time messaging with WebSockets
"""
import json
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List


class ChatConnectionManager:
    """Manages WebSocket connections for real-time chat"""
    
    def __init__(self):
        # Active WebSocket connections by user_id
        self.active_connections: Dict[int, WebSocket] = {}
        # User to building mapping
        self.user_building_map: Dict[int, int] = {}
        # Group chats by building_id
        self.building_groups: Dict[int, List[int]] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        """Accept and store new WebSocket connection"""
        await websocket.accept()
        self.active_connections[user_id] = websocket
        print(f"✅ User {user_id} connected to chat")

    def disconnect(self, user_id: int):
        """Remove disconnected user"""
        if user_id in self.active_connections:
            del self.active_connections[user_id]
            print(f"❌ User {user_id} disconnected")

    def register_building(self, user_id: int, building_id: int):
        """Register user's building for group chats"""
        self.user_building_map[user_id] = building_id
        
        # Add to building group
        if building_id not in self.building_groups:
            self.building_groups[building_id] = []
        if user_id not in self.building_groups[building_id]:
            self.building_groups[building_id].append(user_id)

    async def send_personal(self, receiver_id: int, message: dict):
        """Send message to specific user"""
        if receiver_id in self.active_connections:
            try:
                await self.active_connections[receiver_id].send_text(json.dumps(message))
                print(f"📤 Sent personal message to user {receiver_id}")
            except Exception as e:
                print(f"Error sending personal message: {e}")
        else:
            print(f"⚠️ User {receiver_id} not online")

    async def broadcast_building(self, building_id: int, message: dict):
        """Broadcast message to all users in a building"""
        if building_id in self.building_groups:
            for user_id in self.building_groups[building_id]:
                if user_id in self.active_connections:
                    try:
                        await self.active_connections[user_id].send_text(json.dumps(message))
                        print(f"📢 Broadcast to user {user_id} in building {building_id}")
                    except Exception as e:
                        print(f"Error broadcasting to user {user_id}: {e}")

    async def broadcast_group(self, group_id: str, message: dict):
        """Broadcast to specific group (owner group, etc.)"""
        # Can be extended for custom groups
        pass

    def get_online_users(self) -> List[int]:
        """Get list of currently online users"""
        return list(self.active_connections.keys())

    def is_user_online(self, user_id: int) -> bool:
        """Check if user is online"""
        return user_id in self.active_connections


# Global manager instance
manager = ChatConnectionManager()
