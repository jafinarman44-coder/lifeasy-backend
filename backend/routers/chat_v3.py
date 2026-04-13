# ============================================
# LIFEASY V27+ PHASE 6 STEP 10
# REAL-TIME CHAT ROUTER V3
# ============================================
# Complete chat system with:
# - WebSocket messaging
# - Message history
# - Unread counters
# - Block/unblock
# - Presence tracking
# - Rate limiting
# ============================================

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from datetime import datetime
from typing import List, Optional
import json

from database_prod import get_db
from models import ChatMessage, ChatPresence, ChatUnread, BlockedUser, Tenant, ChatRoom, ChatParticipant
from realtime.chat_socket_manager import chat_manager
from utils.rate_limiter import rate_limiter


router = APIRouter(prefix="/api/chat/v3", tags=["Real-Time Chat V3"])


# ==================== WEBSOCKET ENDPOINT ====================

@router.websocket("/ws/{user_id}/{building_id}")
async def chat_websocket(
    ws: WebSocket,
    user_id: int,
    building_id: int,
    db: Session = Depends(get_db)
):
    """
    Real-time WebSocket for chat messaging
    Handles: messages, typing, presence, receipts
    """
    
    # Connect to chat manager
    await chat_manager.connect(user_id, building_id, ws, db)
    
    try:
        while True:
            raw = await ws.receive_text()
            data = json.loads(raw)
            action = data.get("action")
            
            # RATE LIMIT check (15 messages per 10 seconds)
            if not rate_limiter.allowed(user_id):
                await ws.send_text(json.dumps({
                    "action": "rate_limited",
                    "message": "Too many messages. Please slow down."
                }))
                continue
            
            # ==================== MESSAGE ACTIONS ====================
            
            if action == "send_message":
                # Send message to receiver
                receiver_id = data.get("receiver_id")
                text = data.get("text")
                room_id = data.get("room_id")
                message_type = data.get("message_type", "text")
                media_url = data.get("media_url")
                
                if not receiver_id or not text:
                    await ws.send_text(json.dumps({
                        "action": "error",
                        "message": "Missing receiver_id or text"
                    }))
                    continue
                
                # Send message
                result = await chat_manager.send_message(
                    sender_id=user_id,
                    receiver_id=receiver_id,
                    text=text,
                    db=db,
                    room_id=room_id,
                    message_type=message_type,
                    media_url=media_url
                )
                
                if "error" in result:
                    await ws.send_text(json.dumps(result))
                else:
                    # Confirm to sender
                    await ws.send_text(json.dumps({
                        "action": "message_sent",
                        "message": result
                    }))
            
            elif action == "mark_delivered":
                # Mark messages as delivered
                message_ids = data.get("message_ids", [])
                if message_ids:
                    await chat_manager.mark_delivered(message_ids, db)
            
            elif action == "mark_seen":
                # Mark messages as seen/read
                message_ids = data.get("message_ids", [])
                if message_ids:
                    await chat_manager.mark_seen(message_ids, db)
                    
                    # Confirm to sender
                    for msg_id in message_ids:
                        await ws.send_text(json.dumps({
                            "action": "message_seen",
                            "message_id": msg_id
                        }))
            
            elif action == "typing_start":
                # User started typing
                room_id = data.get("room_id")
                receiver_id = data.get("receiver_id")
                
                if room_id:
                    await chat_manager.set_typing(room_id, user_id, True, db)
            
            elif action == "typing_stop":
                # User stopped typing
                room_id = data.get("room_id")
                
                if room_id:
                    await chat_manager.set_typing(room_id, user_id, False, db)
            
            elif action == "ping":
                # Heartbeat ping
                await ws.send_text(json.dumps({"action": "pong"}))
            
            # ==================== BLOCK ACTIONS ====================
            
            elif action == "block_user":
                blocked_id = data.get("user_id")
                if blocked_id:
                    chat_manager.block_user(user_id, blocked_id, db)
                    await ws.send_text(json.dumps({
                        "action": "user_blocked",
                        "blocked_id": blocked_id
                    }))
            
            elif action == "unblock_user":
                blocked_id = data.get("user_id")
                if blocked_id:
                    chat_manager.unblock_user(user_id, blocked_id, db)
                    await ws.send_text(json.dumps({
                        "action": "user_unblocked",
                        "blocked_id": blocked_id
                    }))
            
            # ==================== CLEANUP ====================
            
            await chat_manager.cleanup()
    
    except WebSocketDisconnect:
        chat_manager.disconnect(user_id, db)
        print(f"💬 User {user_id} disconnected from chat")


# ==================== REST API ENDPOINTS ====================

@router.post("/send")
async def send_message_rest(
    sender_id: int,
    receiver_id: int,
    message: str,
    message_type: str = "text",
    db: Session = Depends(get_db)
):
    """Send a message (REST API for mobile app compatibility)"""
    
    # Check if both users exist
    sender = db.query(Tenant).filter(Tenant.id == sender_id).first()
    receiver = db.query(Tenant).filter(Tenant.id == receiver_id).first()
    
    if not sender:
        raise HTTPException(status_code=404, detail="Sender not found")
    if not receiver:
        raise HTTPException(status_code=404, detail="Receiver not found")
    
    # Create message in database
    chat_message = ChatMessage(
        sender_id=sender_id,
        receiver_id=receiver_id,
        text=message,
        message_type=message_type,
        timestamp=datetime.utcnow()
    )
    db.add(chat_message)
    db.commit()
    db.refresh(chat_message)
    
    print(f"✅ Message saved: {sender.name} -> {receiver.name}: '{message}'")
    
    return {
        "status": "success",
        "message": "Message sent",
        "message_id": chat_message.id
    }

@router.get("/history/{room_id}")
async def get_chat_history(
    room_id: int,
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db)
):
    """Get chat history for a room"""
    
    messages = db.query(ChatMessage).filter(
        ChatMessage.room_id == room_id,
        ChatMessage.deleted_by_sender == False,
        ChatMessage.deleted_by_receiver == False
    ).order_by(
        ChatMessage.timestamp.desc()
    ).offset(offset).limit(limit).all()
    
    return {
        "status": "success",
        "count": len(messages),
        "messages": [
            {
                "id": msg.id,
                "sender_id": msg.sender_id,
                "receiver_id": msg.receiver_id,
                "text": msg.text,
                "timestamp": msg.timestamp.isoformat(),
                "delivered": msg.delivered,
                "seen": msg.seen,
                "message_type": msg.message_type,
                "media_url": msg.media_url
            }
            for msg in reversed(messages)  # Return in chronological order
        ]
    }


@router.get("/conversation/{user_id}")
async def get_conversation(
    user_id: int,
    other_user_id: int,
    limit: int = Query(default=50, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Get conversation between two users"""
    
    messages = db.query(ChatMessage).filter(
        or_(
            and_(ChatMessage.sender_id == user_id, ChatMessage.receiver_id == other_user_id),
            and_(ChatMessage.sender_id == other_user_id, ChatMessage.receiver_id == user_id)
        ),
        ChatMessage.deleted_by_sender == False,
        ChatMessage.deleted_by_receiver == False
    ).order_by(
        ChatMessage.timestamp.desc()
    ).limit(limit).all()
    
    return {
        "status": "success",
        "count": len(messages),
        "messages": [
            {
                "id": msg.id,
                "sender_id": msg.sender_id,
                "receiver_id": msg.receiver_id,
                "text": msg.text,
                "timestamp": msg.timestamp.isoformat(),
                "delivered": msg.delivered,
                "seen": msg.seen
            }
            for msg in reversed(messages)
        ]
    }


@router.get("/unread/count/{user_id}")
async def get_unread_count(user_id: int, db: Session = Depends(get_db)):
    """Get total unread message count for user"""
    
    unread = db.query(ChatUnread).filter(
        ChatUnread.user_id == user_id
    ).first()
    
    return {
        "status": "success",
        "unread_count": unread.unread_count if unread else 0
    }


@router.get("/presence/{user_id}")
async def get_user_presence(user_id: int, db: Session = Depends(get_db)):
    """Get user's online/offline status"""
    
    presence = db.query(ChatPresence).filter(
        ChatPresence.user_id == user_id
    ).first()
    
    is_online = chat_manager.is_user_online(user_id)
    
    return {
        "status": "success",
        "user_id": user_id,
        "online": is_online,
        "last_seen": presence.last_seen.isoformat() if presence and presence.last_seen else None
    }


@router.post("/block/{blocked_id}")
async def block_user(
    blocked_id: int,
    blocker_id: int = Query(...),
    db: Session = Depends(get_db)
):
    """Block a user"""
    
    chat_manager.block_user(blocker_id, blocked_id, db)
    
    return {
        "status": "success",
        "message": f"User {blocked_id} blocked"
    }


@router.post("/unblock/{blocked_id}")
async def unblock_user(
    blocked_id: int,
    blocker_id: int = Query(...),
    db: Session = Depends(get_db)
):
    """Unblock a user"""
    
    chat_manager.unblock_user(blocker_id, blocked_id, db)
    
    return {
        "status": "success",
        "message": f"User {blocked_id} unblocked"
    }


@router.get("/blocked/list/{user_id}")
async def get_blocked_users(user_id: int, db: Session = Depends(get_db)):
    """Get list of blocked users"""
    
    blocks = db.query(BlockedUser).filter(
        BlockedUser.blocker_id == user_id
    ).all()
    
    return {
        "status": "success",
        "blocked_users": [
            {
                "blocked_id": block.blocked_id,
                "blocked_at": block.blocked_at.isoformat()
            }
            for block in blocks
        ]
    }


@router.delete("/message/{message_id}")
async def delete_message(
    message_id: int,
    user_id: int = Query(...),
    delete_for_both: bool = Query(default=False),
    db: Session = Depends(get_db)
):
    """Delete a message (for sender only, or both if admin/owner)"""
    
    message = db.query(ChatMessage).filter(ChatMessage.id == message_id).first()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    # Check if user is sender
    if message.sender_id != user_id:
        # Check if user is owner/admin (can delete for both)
        tenant = db.query(Tenant).filter(Tenant.id == user_id).first()
        if not tenant or tenant.role not in ['owner', 'admin']:
            delete_for_both = False
    
    if delete_for_both:
        message.deleted_by_sender = True
        message.deleted_by_receiver = True
    else:
        message.deleted_by_sender = True
    
    db.commit()
    
    return {
        "status": "success",
        "message": "Message deleted"
    }
