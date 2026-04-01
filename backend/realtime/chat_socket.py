"""
LIFEASY V30 PRO - High Performance Chat Socket Manager v3
Multi-room architecture with building-based grouping
"""
import json
from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List


class ChatManager:
    """High-performance chat connection manager with multi-room support"""
    
    def __init__(self):
        # Direct connections: {user_id: websocket}
        self.connections: Dict[int, WebSocket] = {}
        # Building-based rooms: {building_id: {user_id: ws}}
        self.rooms: Dict[int, Dict[int, WebSocket]] = {}
        # User to building mapping
        self.user_building_map: Dict[int, int] = {}

    async def connect(self, user_id: int, building_id: int, ws: WebSocket):
        """Accept and store new WebSocket connection with building context"""
        await ws.accept()
        
        # Store direct connection
        self.connections[user_id] = ws
        
        # Add to building room
        self.rooms.setdefault(building_id, {})[user_id] = ws
        
        # Map user to building
        self.user_building_map[user_id] = building_id
        
        print(f"🟢 Chat connect: User {user_id} in Building {building_id}")
        print(f"   Total connections: {len(self.connections)}")
        print(f"   Building {building_id} users: {len(self.rooms.get(building_id, {}))}")

    def disconnect(self, user_id: int):
        """Remove disconnected user from all rooms"""
        # Remove from direct connections
        if user_id in self.connections:
            del self.connections[user_id]
        
        # Remove from all building rooms
        for building_users in self.rooms.values():
            building_users.pop(user_id, None)
        
        # Clean up empty rooms
        empty_buildings = [b for b, users in self.rooms.items() if not users]
        for building in empty_buildings:
            del self.rooms[building]
        
        # Remove building mapping
        if user_id in self.user_building_map:
            del self.user_building_map[user_id]
        
        print(f"🔴 Chat disconnect: User {user_id}")
        print(f"   Remaining connections: {len(self.connections)}")

    async def send(self, user_id: int, data: dict):
        """Send JSON message to specific user"""
        ws = self.connections.get(user_id)
        if ws:
            try:
                await ws.send_json(data)
                print(f"📤 Sent to user {user_id}: {data.get('action')}")
            except Exception as e:
                print(f"Error sending to user {user_id}: {e}")
                self.disconnect(user_id)
        else:
            print(f"⚠️ User {user_id} not online")

    async def broadcast_building(self, building_id: int, data: dict, exclude: int | None = None):
        """Broadcast message to all users in a building"""
        if building_id not in self.rooms:
            return
        
        for user_id, ws in list(self.rooms[building_id].items()):
            if user_id != exclude:  # Optionally exclude sender
                try:
                    await ws.send_json(data)
                    print(f"📢 Broadcast to user {user_id} in building {building_id}")
                except Exception as e:
                    print(f"Error broadcasting to user {user_id}: {e}")
                    self.disconnect(user_id)

    async def broadcast_group(self, user_ids: List[int], data: dict):
        """Broadcast to specific group of users"""
        for user_id in user_ids:
            await self.send(user_id, data)

    def is_online(self, user_id: int) -> bool:
        """Check if user is currently connected"""
        return user_id in self.connections

    def get_online_users(self) -> List[int]:
        """Get list of all online users"""
        return list(self.connections.keys())

    def get_building_users(self, building_id: int) -> List[int]:
        """Get all online users in a building"""
        if building_id not in self.rooms:
            return []
        return list(self.rooms[building_id].keys())

    def get_user_building(self, user_id: int) -> int | None:
        """Get building ID for a user"""
        return self.user_building_map.get(user_id)

    def get_stats(self) -> dict:
        """Get chat manager statistics"""
        return {
            "total_connections": len(self.connections),
            "total_buildings": len(self.rooms),
            "buildings": {
                building_id: len(users)
                for building_id, users in self.rooms.items()
            }
        }


# Global chat manager instance
chat_manager = ChatManager()
