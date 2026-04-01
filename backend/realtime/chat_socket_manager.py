# ============================================
# LIFEASY V27+ PHASE 6 STEP 10
# REAL-TIME CHAT SOCKET MANAGER
# ============================================
# Production-grade chat system with:
# - WebSocket messaging
# - Presence tracking (online/offline)
# - Message queuing for offline users
# - Delivery & Seen receipts
# - Typing indicators
# - Block/unblock system
# - Rate limiting (anti-spam)
# ============================================

from typing import Dict, List
from fastapi import WebSocket
from sqlalchemy.orm import Session
from sqlalchemy import or_
from datetime import datetime, timedelta
import json
import time

from models import ChatMessage, ChatPresence, ChatUnread, BlockedUser, Tenant, ChatRoom, ChatParticipant
from realtime.message_queue import message_queue
from realtime.rate_limiter import rate_limiter


class ChatSocketManager:
    """
    Real-time Chat Socket Manager
    Handles all chat-related WebSocket operations
    """
    
    def __init__(self):
        # Active connections: {user_id: WebSocket}
        self.active_connections: Dict[int, WebSocket] = {}
        
        # User presence: {user_id: status}
        self.user_presence: Dict[int, str] = {}
        
        # Typing indicators: {(room_id, user_id): is_typing}
        self.typing_users: Dict[tuple, bool] = {}
        
        # Rate limiter: 15 messages per 10 seconds
        self.rate_limiter = rate_limiter
    
    # ==================== CONNECTION MANAGEMENT ====================
    
    async def connect(self, user_id: int, building_id: int, ws: WebSocket, db: Session):
        """Accept new WebSocket connection and set user online"""
        await ws.accept()
        self.active_connections[user_id] = ws
        
        # Update presence to online
        await self.set_online(user_id, building_id, db)
        
        # Deliver queued messages
        await self.deliver_queued_messages(user_id, ws, db)
        
        print(f"💬 Chat user {user_id} connected (Building {building_id})")
    
    def disconnect(self, user_id: int, db: Session):
        """Remove disconnected user and set offline"""
        if user_id in self.active_connections:
            del self.active_connections[user_id]
        
        # Update presence to offline
        self.set_offline(user_id, db)
        
        print(f"💬 Chat user {user_id} disconnected")
    
    # ==================== PRESENCE SYSTEM ====================
    
    async def set_online(self, user_id: int, building_id: int, db: Session):
        """Set user status to online"""
        presence = db.query(ChatPresence).filter(ChatPresence.user_id == user_id).first()
        
        if not presence:
            presence = ChatPresence(
                user_id=user_id,
                status='online',
                building_id=building_id
            )
            db.add(presence)
        else:
            presence.status = 'online'
            presence.last_seen = datetime.utcnow()
        
        db.commit()
        self.user_presence[user_id] = 'online'
        
        # Broadcast online status to building
        await self.broadcast_presence(user_id, 'online', building_id, db)
    
    def set_offline(self, user_id: int, db: Session):
        """Set user status to offline"""
        presence = db.query(ChatPresence).filter(ChatPresence.user_id == user_id).first()
        
        if presence:
            presence.status = 'offline'
            presence.last_seen = datetime.utcnow()
            db.commit()
        
        self.user_presence[user_id] = 'offline'
    
    def is_user_online(self, user_id: int) -> bool:
        """Check if user is currently online"""
        return user_id in self.active_connections
    
    def get_user_status(self, user_id: int) -> str:
        """Get user's current status (online/offline/away)"""
        if user_id in self.active_connections:
            return 'online'
        return 'offline'
    
    # ==================== MESSAGE DELIVERY ====================
    
    async def deliver_queued_messages(self, user_id: int, ws: WebSocket, db: Session):
        """Deliver buffered messages from offline period"""
        queued = message_queue.pop_all(user_id)
        
        for msg_data in queued:
            try:
                await ws.send_text(json.dumps(msg_data))
                print(f"📤 Delivered queued message to user {user_id}")
            except Exception as e:
                print(f"Error delivering queued message: {e}")
    
    async def send_message(
        self, 
        sender_id: int, 
        receiver_id: int, 
        text: str,
        db: Session,
        room_id: int = None,
        message_type: str = 'text',
        media_url: str = None
    ) -> dict:
        """
        Send message from sender to receiver
        Returns message data dict
        """
        # Check if sender blocked receiver
        is_blocked = db.query(BlockedUser).filter(
            or_(
                (BlockedUser.blocker_id == receiver_id) & (BlockedUser.blocked_id == sender_id),
                (BlockedUser.blocker_id == sender_id) & (BlockedUser.blocked_id == receiver_id)
            )
        ).first()
        
        if is_blocked:
            return {"error": "blocked", "message": "Cannot send message - you're blocked"}
        
        # Create message record
        message = ChatMessage(
            sender_id=sender_id,
            receiver_id=receiver_id,
            room_id=room_id,
            text=text,
            message_type=message_type,
            media_url=media_url
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        
        # Prepare message data
        message_data = {
            "action": "new_message",
            "message": {
                "id": message.id,
                "sender_id": sender_id,
                "receiver_id": receiver_id,
                "text": text,
                "timestamp": message.timestamp.isoformat(),
                "delivered": False,
                "seen": False,
                "message_type": message_type,
                "media_url": media_url
            }
        }
        
        # Send to receiver if online
        if receiver_id in self.active_connections:
            try:
                await self.active_connections[receiver_id].send_text(json.dumps(message_data))
                message.delivered = True
                db.commit()
                print(f"📤 Sent message to online user {receiver_id}")
            except Exception as e:
                print(f"Error sending message: {e}")
                message_queue.add_message(receiver_id, message_data)
        else:
            # Queue message for offline user
            message_queue.add_message(receiver_id, message_data)
            print(f"💾 Queued message for offline user {receiver_id}")
        
        # Update unread counter
        self._increment_unread(receiver_id, room_id, db)
        
        return message_data["message"]
    
    # ==================== DELIVERY & SEEN RECEIPTS ====================
    
    async def mark_delivered(self, message_ids: List[int], db: Session):
        """Mark messages as delivered"""
        db.query(ChatMessage).filter(
            ChatMessage.id.in_(message_ids)
        ).update({"delivered": True}, synchronize_session=False)
        db.commit()
    
    async def mark_seen(self, message_ids: List[int], db: Session):
        """Mark messages as seen/read"""
        db.query(ChatMessage).filter(
            ChatMessage.id.in_(message_ids)
        ).update({"seen": True}, synchronize_session=False)
        db.commit()
        
        # Clear unread counter
        if message_ids:
            last_msg_id = max(message_ids)
            # Get room from first message
            msg = db.query(ChatMessage).filter(ChatMessage.id == message_ids[0]).first()
            if msg:
                self._clear_unread(msg.receiver_id, msg.room_id, db)
    
    # ==================== TYPING INDICATORS ====================
    
    async def set_typing(self, room_id: int, user_id: int, is_typing: bool, db: Session):
        """Set typing indicator for user in room"""
        key = (room_id, user_id)
        self.typing_users[key] = is_typing
        
        # Get other participants in room
        participants = await self._get_room_participants(room_id, db)
        
        # Broadcast typing status to room
        for participant_id in participants:
            if participant_id != user_id and participant_id in self.active_connections:
                try:
                    await self.active_connections[participant_id].send_text(json.dumps({
                        "action": "typing_indicator",
                        "room_id": room_id,
                        "user_id": user_id,
                        "is_typing": is_typing
                    }))
                except Exception as e:
                    print(f"Error broadcasting typing: {e}")
    
    # ==================== BLOCK/UNBLOCK SYSTEM ====================
    
    def block_user(self, blocker_id: int, blocked_id: int, db: Session):
        """Block a user"""
        existing = db.query(BlockedUser).filter(
            BlockedUser.blocker_id == blocker_id,
            BlockedUser.blocked_id == blocked_id
        ).first()
        
        if not existing:
            block = BlockedUser(
                blocker_id=blocker_id,
                blocked_id=blocked_id
            )
            db.add(block)
            db.commit()
            print(f"🚫 User {blocker_id} blocked {blocked_id}")
    
    def unblock_user(self, blocker_id: int, blocked_id: int, db: Session):
        """Unblock a user"""
        block = db.query(BlockedUser).filter(
            BlockedUser.blocker_id == blocker_id,
            BlockedUser.blocked_id == blocked_id
        ).first()
        
        if block:
            db.delete(block)
            db.commit()
            print(f"✅ User {blocker_id} unblocked {blocked_id}")
    
    def is_blocked(self, user1_id: int, user2_id: int, db: Session) -> bool:
        """Check if one user has blocked another"""
        block = db.query(BlockedUser).filter(
            or_(
                (BlockedUser.blocker_id == user1_id) & (BlockedUser.blocked_id == user2_id),
                (BlockedUser.blocker_id == user2_id) & (BlockedUser.blocked_id == user1_id)
            )
        ).first()
        
        return block is not None
    
    # ==================== BROADCAST TO BUILDING ====================
    
    async def broadcast_to_building(self, building_id: int, message: dict, db: Session):
        """Broadcast message to all users in a building"""
        # Get all users in building
        users = db.query(Tenant).filter(Tenant.building == building_id).all()
        
        for user in users:
            if user.id in self.active_connections:
                try:
                    await self.active_connections[user.id].send_text(json.dumps(message))
                except Exception as e:
                    print(f"Error broadcasting to user {user.id}: {e}")
    
    async def broadcast_presence(self, user_id: int, status: str, building_id: int, db: Session):
        """Broadcast user's presence status to their building"""
        presence_data = {
            "action": "presence_update",
            "user_id": user_id,
            "status": status,
            "building_id": building_id
        }
        
        await self.broadcast_to_building(building_id, presence_data, db)
    
    # ==================== HELPER METHODS ====================
    
    def _increment_unread(self, user_id: int, room_id: int, db: Session):
        """Increment unread counter for user"""
        unread = db.query(ChatUnread).filter(
            ChatUnread.user_id == user_id,
            ChatUnread.room_id == room_id
        ).first()
        
        if not unread:
            unread = ChatUnread(
                user_id=user_id,
                room_id=room_id,
                unread_count=1
            )
            db.add(unread)
        else:
            unread.unread_count += 1
            unread.updated_at = datetime.utcnow()
        
        db.commit()
    
    def _clear_unread(self, user_id: int, room_id: int, db: Session):
        """Clear unread counter for user"""
        unread = db.query(ChatUnread).filter(
            ChatUnread.user_id == user_id,
            ChatUnread.room_id == room_id
        ).first()
        
        if unread:
            unread.unread_count = 0
            db.commit()
    
    async def _get_room_participants(self, room_id: int, db: Session) -> List[int]:
        """Get list of participant IDs in a room"""
        participants = db.query(ChatParticipant).filter(
            ChatParticipant.room_id == room_id
        ).all()
        
        return [p.tenant_id for p in participants]
    
    async def cleanup(self):
        """Periodic cleanup of stale data"""
        # Clean old typing indicators (older than 10 seconds)
        now = datetime.utcnow()
        expired = now - timedelta(seconds=10)
        
        for key in list(self.typing_users.keys()):
            if self.typing_users[key]:
                self.typing_users[key] = False


# Global chat manager instance
chat_manager = ChatSocketManager()
