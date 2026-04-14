"""
LIFEASY V27+ PHASE 6 STEP 4 - Chat Router with REST + WebSockets
Complete chat system with real-time messaging, file sharing, and calls
"""
from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlalchemy.orm import Session
from database_prod import get_db
from models import ChatMessage, ChatRoom, ChatParticipant, BlockedUser, Tenant, CallLog
from chat_socket import manager
from realtime.message_queue import message_queue
from datetime import datetime
from typing import Optional
import json

router = APIRouter(prefix="/api/chat", tags=["Chat System"])


# ==================== WEBSOCKET ENDPOINT ====================

@router.websocket("/ws/{user_id}/{building_id}")
async def chat_websocket(
    websocket: WebSocket,
    user_id: int,
    building_id: int,
    db: Session = Depends(get_db)
):
    """
    Real-time WebSocket chat endpoint
    Handles personal messages, group messages, and call signaling
    """
    # Register user's building
    manager.register_building(user_id, building_id)
    
    # Connect to WebSocket
    await manager.connect(user_id, websocket)
    
    # Send any buffered messages from when user was offline
    queued = message_queue.pop_all(user_id)
    for msg in queued:
        try:
            await websocket.send_text(msg)
        except Exception as e:
            print(f"Error sending queued message: {e}")
    
    try:
        while True:
            # Receive message
            text = await websocket.receive_text()
            data = json.loads(text)
            
            # Parse message
            sender_id = data.get('sender_id')
            receiver_id = data.get('receiver_id')
            message = data.get('message', '')
            message_type = data.get('message_type', 'text')  # text, image, audio, video, call, group
            file_url = data.get('file_url')
            room_id = data.get('room_id')
            
            # Check if sender is blocked by receiver
            is_blocked = db.query(BlockedUser).filter(
                BlockedUser.blocker_id == receiver_id,
                BlockedUser.blocked_id == sender_id
            ).first()
            
            if is_blocked and message_type != 'call':
                # Don't deliver message if blocked (except call signaling)
                await websocket.send_text(json.dumps({
                    'status': 'blocked',
                    'message': 'Message not delivered - you are blocked'
                }))
                continue
            
            # Create chat message object
            chat_msg = {
                'sender_id': sender_id,
                'receiver_id': receiver_id,
                'message': message,
                'message_type': message_type,
                'file_url': file_url,
                'room_id': room_id,
                'building_id': building_id,
                'timestamp': datetime.utcnow().isoformat(),
                'delivered': True
            }
            
            # Save to database
            try:
                if message_type in ['text', 'image', 'audio', 'video']:
                    db_message = ChatMessage(
                        room_id=room_id or 0,
                        sender_id=sender_id,
                        message=message,
                        created_at=datetime.utcnow()
                    )
                    db.add(db_message)
                    db.commit()
                    chat_msg['id'] = db_message.id
            except Exception as e:
                print(f"Error saving message to DB: {e}")
                db.rollback()
            
            # Send to receiver (if personal message)
            if receiver_id and message_type != 'group':
                await manager.send_personal(receiver_id, chat_msg)
            
            # Broadcast to building (if group message)
            elif message_type == 'group':
                await manager.broadcast_building(building_id, chat_msg)
            
            # Acknowledge to sender
            await websocket.send_text(json.dumps({
                'status': 'sent',
                'id': chat_msg.get('id'),
                **chat_msg
            }))
            
    except WebSocketDisconnect:
        manager.disconnect(user_id)
        # Notify others about disconnect (optional)


# ==================== REST API ENDPOINTS ====================

@router.get("/history/{room_id}")
def get_chat_history(room_id: int, limit: int = 50, db: Session = Depends(get_db)):
    """Get chat history for a room"""
    try:
        messages = db.query(ChatMessage).filter(
            ChatMessage.room_id == room_id
        ).order_by(ChatMessage.created_at.desc()).limit(limit).all()
        
        return {
            'status': 'success',
            'count': len(messages),
            'messages': [
                {
                    'id': msg.id,
                    'sender_id': msg.sender_id,
                    'message': msg.message,
                    'created_at': msg.created_at.isoformat() if msg.created_at else None,
                }
                for msg in messages
            ]
        }
    except Exception as e:
        print(f"❌ ERROR in get_chat_history: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching chat history: {str(e)}"
        )


@router.get("/rooms/{tenant_id}")
def get_user_rooms(tenant_id: int, db: Session = Depends(get_db)):
    """Get all chat rooms for a user"""
    participants = db.query(ChatParticipant).filter(
        ChatParticipant.tenant_id == tenant_id
    ).all()
    
    room_ids = [p.room_id for p in participants]
    rooms = db.query(ChatRoom).filter(ChatRoom.id.in_(room_ids)).all()
    
    return {
        'status': 'success',
        'count': len(rooms),
        'rooms': [
            {
                'id': room.id,
                'is_group': room.is_group,
            }
            for room in rooms
        ]
    }


@router.post("/send")
def send_message(
    sender_id: int,
    receiver_id: int,
    message: str,
    message_type: str = "text",
    file_url: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Send message via REST (fallback if WebSocket unavailable)"""
    # Check if blocked
    is_blocked = db.query(BlockedUser).filter(
        BlockedUser.blocker_id == receiver_id,
        BlockedUser.blocked_id == sender_id
    ).first()
    
    if is_blocked:
        raise HTTPException(status_code=403, detail="You are blocked by this user")
    
    # Get or create room
    room = get_or_create_room(db, sender_id, receiver_id)
    
    # Save message
    db_message = ChatMessage(
        room_id=room.id,
        sender_id=sender_id,
        message=message,
        created_at=datetime.utcnow()
    )
    db.add(db_message)
    db.commit()
    
    # Try to send via WebSocket if receiver is online
    if manager.is_user_online(receiver_id):
        import asyncio
        asyncio.create_task(manager.send_personal(receiver_id, {
            'id': db_message.id,
            'sender_id': sender_id,
            'message': message,
            'message_type': message_type,
            'file_url': file_url,
            'room_id': room.id,
            'timestamp': datetime.utcnow().isoformat(),
        }))
    
    return {
        'status': 'sent',
        'message_id': db_message.id,
        'room_id': room.id
    }


def get_or_create_room(db: Session, user1_id: int, user2_id: int) -> ChatRoom:
    """Get existing room or create new one"""
    # Find common rooms
    user1_rooms = db.query(ChatParticipant.room_id).filter(
        ChatParticipant.tenant_id == user1_id
    ).all()
    
    user2_rooms = db.query(ChatParticipant.room_id).filter(
        ChatParticipant.tenant_id == user2_id
    ).all()
    
    common_room_ids = set([r[0] for r in user1_rooms]) & set([r[0] for r in user2_rooms])
    
    if common_room_ids:
        return db.query(ChatRoom).filter(ChatRoom.id == list(common_room_ids)[0]).first()
    
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
