"""
LIFEASY V27 - Group Chat WebSocket Manager
Real-time group messaging with multi-user support
"""
from fastapi import WebSocket
from typing import Dict, List
import json
from datetime import datetime

class GroupChatManager:
    """
    Manages real-time group chat WebSocket connections
    Handles message broadcasting to all group members
    """
    
    def __init__(self):
        # Active connections: {user_id: WebSocket}
        self.active_connections: Dict[int, WebSocket] = {}
        
        # User's current group rooms: {user_id: [room_ids]}
        self.user_rooms: Dict[int, List[int]] = {}
        
        # Room members: {room_id: [user_ids]}
        self.room_members: Dict[int, List[int]] = {}
    
    # ==================== CONNECTION MANAGEMENT ====================
    
    async def connect(self, user_id: int, ws: WebSocket, room_ids: List[int]):
        """Accept WebSocket connection and join user to their groups"""
        await ws.accept()
        self.active_connections[user_id] = ws
        self.user_rooms[user_id] = room_ids
        
        # Add user to room member lists
        for room_id in room_ids:
            if room_id not in self.room_members:
                self.room_members[room_id] = []
            if user_id not in self.room_members[room_id]:
                self.room_members[room_id].append(user_id)
        
        print(f"👥 User {user_id} connected to groups: {room_ids}")
        
        # Notify rooms of user's presence
        await self.broadcast_to_rooms(user_id, {
            "action": "user_online",
            "user_id": user_id,
            "room_ids": room_ids
        })
    
    def disconnect(self, user_id: int):
        """Remove disconnected user and update room memberships"""
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        
        # Get user's rooms before removing
        user_room_list = self.user_rooms.get(user_id, [])
        
        # Remove from room memberships
        for room_id in user_room_list:
            if room_id in self.room_members:
                if user_id in self.room_members[room_id]:
                    self.room_members[room_id].remove(user_id)
        
        # Remove user's room mapping
        if user_id in self.user_rooms:
            del self.user_rooms[user_id]
        
        print(f"👥 User {user_id} disconnected from groups")
    
    def is_user_online(self, user_id: int) -> bool:
        """Check if user is currently connected"""
        return user_id in self.active_connections
    
    # ==================== MESSAGE BROADCASTING ====================
    
    async def send_group_message(
        self,
        room_id: int,
        sender_id: int,
        message_data: dict
    ):
        """
        Broadcast message to all members in a group room
        Excludes the sender
        """
        # Get all members in this room
        room_members = self.room_members.get(room_id, [])
        
        # Remove sender from list (don't send to self)
        receivers = [uid for uid in room_members if uid != sender_id]
        
        # Prepare broadcast message
        broadcast_data = {
            "action": "group_message",
            "room_id": room_id,
            "sender_id": sender_id,
            "message": message_data,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Send to all online members
        sent_count = 0
        for receiver_id in receivers:
            if receiver_id in self.active_connections:
                try:
                    await self.active_connections[receiver_id].send_text(
                        json.dumps(broadcast_data)
                    )
                    sent_count += 1
                except Exception as e:
                    print(f"Error sending to user {receiver_id}: {e}")
        
        print(f"📢 Broadcast group message to {sent_count}/{len(receivers)} members")
    
    async def broadcast_to_rooms(self, user_id: int, data: dict):
        """Broadcast event to all rooms user is member of"""
        user_rooms = self.user_rooms.get(user_id, [])
        
        for room_id in user_rooms:
            await self.broadcast_to_room(room_id, data, exclude_user=user_id)
    
    async def broadcast_to_room(self, room_id: int, data: dict, exclude_user: int = None):
        """Broadcast event to all members in a room"""
        room_members = self.room_members.get(room_id, [])
        
        for member_id in room_members:
            if member_id != exclude_user and member_id in self.active_connections:
                try:
                    await self.active_connections[member_id].send_text(json.dumps(data))
                except Exception as e:
                    print(f"Error broadcasting to {member_id}: {e}")
    
    # ==================== GROUP EVENTS ====================
    
    async def notify_member_added(self, room_id: int, new_member_id: int, added_by: int):
        """Notify group that a new member was added"""
        await self.broadcast_to_room(room_id, {
            "action": "group_member_added",
            "room_id": room_id,
            "new_member_id": new_member_id,
            "added_by": added_by
        })
    
    async def notify_member_removed(self, room_id: int, removed_member_id: int, removed_by: int):
        """Notify group that a member was removed"""
        await self.broadcast_to_room(room_id, {
            "action": "group_member_removed",
            "room_id": room_id,
            "removed_member_id": removed_member_id,
            "removed_by": removed_by
        }, exclude_user=removed_member_id)
    
    # ==================== GROUP CALL SIGNALING ====================
    
    async def send_group_call_offer(
        self,
        room_id: int,
        caller_id: int,
        call_data: dict
    ):
        """Broadcast call offer to all group members"""
        await self.broadcast_to_room(room_id, {
            "action": "group_call_offer",
            "room_id": room_id,
            "caller_id": caller_id,
            "call_data": call_data
        }, exclude_user=caller_id)
    
    async def send_group_call_answer(
        self,
        room_id: int,
        responder_id: int,
        answer_data: dict
    ):
        """Broadcast call answer to group"""
        await self.broadcast_to_room(room_id, {
            "action": "group_call_answer",
            "room_id": room_id,
            "responder_id": responder_id,
            "answer_data": answer_data
        })
    
    async def send_group_call_end(
        self,
        room_id: int,
        user_id: int,
        reason: str = "ended"
    ):
        """Broadcast call end to group"""
        await self.broadcast_to_room(room_id, {
            "action": "group_call_end",
            "room_id": room_id,
            "user_id": user_id,
            "reason": reason
        })
    
    # ==================== TYPING INDICATORS ====================
    
    async def broadcast_typing(self, room_id: int, user_id: int, is_typing: bool):
        """Broadcast typing indicator to group"""
        await self.broadcast_to_room(room_id, {
            "action": "group_typing",
            "room_id": room_id,
            "user_id": user_id,
            "is_typing": is_typing
        }, exclude_user=user_id)
    
    # ==================== HELPER METHODS ====================
    
    def get_online_members(self, room_id: int) -> List[int]:
        """Get list of online members in a room"""
        room_members = self.room_members.get(room_id, [])
        return [uid for uid in room_members if uid in self.active_connections]
    
    def get_room_member_count(self, room_id: int) -> int:
        """Get total member count for a room"""
        return len(self.room_members.get(room_id, []))
    
    def get_online_room_count(self, room_id: int) -> int:
        """Get count of online members in a room"""
        return len(self.get_online_members(room_id))


# Global instance
group_chat_manager = GroupChatManager()
