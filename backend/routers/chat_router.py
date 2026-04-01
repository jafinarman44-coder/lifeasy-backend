"""
LIFEASY V27+ PHASE 6 - Chat System API
WhatsApp-style messaging with block/unblock functionality
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database_prod import get_db
from models import ChatRoom, ChatParticipant, ChatMessage, BlockedUser, Tenant
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

router = APIRouter(prefix="/api/chat", tags=["Chat"])


class SendMessageRequest(BaseModel):
    sender_id: int
    receiver_id: int
    message: str


class ChatMessageResponse(BaseModel):
    id: int
    room_id: int
    sender_id: int
    message: str
    created_at: datetime
    sender_name: Optional[str]


class BlockUserRequest(BaseModel):
    me: int  # The user who is blocking
    user: int  # The user being blocked


class GetMessagesRequest(BaseModel):
    room_id: int
    limit: Optional[int] = 50


@router.post("/send")
def send_message(data: SendMessageRequest, db: Session = Depends(get_db)):
    """
    Send a message to another tenant
    Checks if sender is blocked by receiver
    """
    sender_id = data.sender_id
    receiver_id = data.receiver_id
    message_text = data.message
    
    # Check if receiver has blocked sender
    is_blocked = db.query(BlockedUser).filter(
        BlockedUser.blocker_id == receiver_id,
        BlockedUser.blocked_id == sender_id
    ).first()
    
    if is_blocked:
        return {
            "status": "blocked",
            "message": "You cannot send messages to this user (you are blocked)"
        }
    
    # Get or create chat room
    room = get_or_create_chat_room(db, sender_id, receiver_id)
    
    # Save message
    chat_message = ChatMessage(
        room_id=room.id,
        sender_id=sender_id,
        message=message_text
    )
    
    db.add(chat_message)
    db.commit()
    db.refresh(chat_message)
    
    # Get sender info
    sender = db.query(Tenant).filter(Tenant.id == sender_id).first()
    
    return {
        "status": "sent",
        "message": "Message sent successfully",
        "data": {
            "id": chat_message.id,
            "room_id": room.id,
            "sender_id": sender_id,
            "message": message_text,
            "created_at": chat_message.created_at.isoformat(),
            "sender_name": sender.name if sender else "Unknown"
        }
    }


@router.get("/messages/{room_id}")
def get_messages(room_id: int, limit: int = 50, db: Session = Depends(get_db)):
    """
    Get chat messages for a room
    """
    messages = db.query(ChatMessage).filter(
        ChatMessage.room_id == room_id
    ).order_by(ChatMessage.created_at.desc()).limit(limit).all()
    
    # Reverse to get chronological order
    messages.reverse()
    
    return {
        "status": "success",
        "room_id": room_id,
        "count": len(messages),
        "messages": [
            {
                "id": msg.id,
                "room_id": msg.room_id,
                "sender_id": msg.sender_id,
                "message": msg.message,
                "created_at": msg.created_at.isoformat()
            }
            for msg in messages
        ]
    }


@router.post("/block")
def block_user(data: BlockUserRequest, db: Session = Depends(get_db)):
    """
    Block a user from sending you messages
    """
    blocker_id = data.me
    blocked_id = data.user
    
    # Verify both users exist
    blocker = db.query(Tenant).filter(Tenant.id == blocker_id).first()
    blocked = db.query(Tenant).filter(Tenant.id == blocked_id).first()
    
    if not blocker or not blocked:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "error", "message": "User not found"}
        )
    
    # Check if already blocked
    existing_block = db.query(BlockedUser).filter(
        BlockedUser.blocker_id == blocker_id,
        BlockedUser.blocked_id == blocked_id
    ).first()
    
    if existing_block:
        return {
            "status": "already_blocked",
            "message": "User is already blocked"
        }
    
    # Create block record
    block_record = BlockedUser(
        blocker_id=blocker_id,
        blocked_id=blocked_id
    )
    
    db.add(block_record)
    db.commit()
    
    return {
        "status": "success",
        "message": "User blocked successfully"
    }


@router.post("/unblock")
def unblock_user(data: BlockUserRequest, db: Session = Depends(get_db)):
    """
    Unblock a previously blocked user
    """
    blocker_id = data.me
    blocked_id = data.user
    
    # Find and delete block record
    block_record = db.query(BlockedUser).filter(
        BlockedUser.blocker_id == blocker_id,
        BlockedUser.blocked_id == blocked_id
    ).first()
    
    if not block_record:
        return {
            "status": "not_blocked",
            "message": "User is not blocked"
        }
    
    db.delete(block_record)
    db.commit()
    
    return {
        "status": "success",
        "message": "User unblocked successfully"
    }


@router.get("/blocked-list/{tenant_id}")
def get_blocked_list(tenant_id: int, db: Session = Depends(get_db)):
    """
    Get list of users blocked by a tenant
    """
    blocked_users = db.query(BlockedUser, Tenant).join(
        Tenant, BlockedUser.blocked_id == Tenant.id
    ).filter(
        BlockedUser.blocker_id == tenant_id
    ).all()
    
    return {
        "status": "success",
        "count": len(blocked_users),
        "blocked_users": [
            {
                "id": bu.Tenant.id,
                "name": bu.Tenant.name,
                "email": bu.Tenant.email
            }
            for bu in blocked_users
        ]
    }


@router.get("/rooms/{tenant_id}")
def get_chat_rooms(tenant_id: int, db: Session = Depends(get_db)):
    """
    Get all chat rooms for a tenant
    """
    # Get all participant records for this tenant
    participants = db.query(ChatParticipant).filter(
        ChatParticipant.tenant_id == tenant_id
    ).all()
    
    room_ids = [p.room_id for p in participants]
    
    # Get rooms
    rooms = db.query(ChatRoom).filter(ChatRoom.id.in_(room_ids)).all()
    
    return {
        "status": "success",
        "count": len(rooms),
        "rooms": [
            {
                "id": room.id,
                "is_group": room.is_group
            }
            for room in rooms
        ]
    }


# Helper function
def get_or_create_chat_room(db: Session, user1_id: int, user2_id: int) -> ChatRoom:
    """
    Get existing chat room between two users or create new one
    """
    # Find all rooms where both users are participants
    user1_rooms = db.query(ChatParticipant.room_id).filter(
        ChatParticipant.tenant_id == user1_id
    ).all()
    
    user2_rooms = db.query(ChatParticipant.room_id).filter(
        ChatParticipant.tenant_id == user2_id
    ).all()
    
    # Find common rooms
    common_room_ids = set([r[0] for r in user1_rooms]) & set([r[0] for r in user2_rooms])
    
    if common_room_ids:
        # Return first common room
        room_id = list(common_room_ids)[0]
        return db.query(ChatRoom).filter(ChatRoom.id == room_id).first()
    
    # Create new room
    room = ChatRoom(is_group=False)
    db.add(room)
    db.commit()
    db.refresh(room)
    
    # Add participants
    participant1 = ChatParticipant(room_id=room.id, tenant_id=user1_id)
    participant2 = ChatParticipant(room_id=room.id, tenant_id=user2_id)
    
    db.add(participant1)
    db.add(participant2)
    db.commit()
    
    return room
