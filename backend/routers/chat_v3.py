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
#
# FIXED: WebSocket database session management
# FIXED: HTTP API accepts JSON body
# FIXED: Proper error handling
# ============================================

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from datetime import datetime
from typing import List, Optional
import json
from pydantic import BaseModel

from database_prod import get_db
from models import ChatMessage, ChatPresence, ChatUnread, BlockedUser, Tenant, ChatRoom, ChatParticipant
from realtime.chat_socket_manager import chat_manager
from utils.rate_limiter import rate_limiter


router = APIRouter(prefix="/api/chat/v3", tags=["Real-Time Chat V3"])

# Request models for HTTP endpoints
class SendMessageRequest(BaseModel):
    sender_id: int
    receiver_id: int
    message: str
    message_type: str = "text"
    media_url: Optional[str] = None


# ==================== WEBSOCKET ENDPOINT ====================

@router.websocket("/ws/{user_id}/{building_id}")
async def chat_websocket(
    ws: WebSocket,
    user_id: int,
    building_id: int
):
    """
    Real-time WebSocket for chat messaging
    Handles: messages, typing, presence, receipts
    
    FIXED: Manual database session management (Depends doesn't work with WebSocket)
    FIXED: Proper error handling to prevent immediate disconnect
    """
    
    # Step 1: Accept WebSocket connection FIRST
    await ws.accept()
    
    # Step 2: Create database session manually (not using Depends)
    db = next(get_db())
    
    try:
        # Step 3: Connect to chat manager with valid db session
        await chat_manager.connect(user_id, building_id, ws, db)
        
        # Step 4: Main message loop
        while True:
            try:
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
                    
                    try:
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
                    except Exception as e:
                        print(f"❌ Error sending message: {e}")
                        import traceback
                        traceback.print_exc()
                        await ws.send_text(json.dumps({
                            "action": "error",
                            "message": f"Failed to send message: {str(e)}"
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
            
            except json.JSONDecodeError:
                await ws.send_text(json.dumps({
                    "action": "error",
                    "message": "Invalid JSON format"
                }))
            except Exception as e:
                print(f"❌ WebSocket message error: {e}")
                import traceback
                traceback.print_exc()
                await ws.send_text(json.dumps({
                    "action": "error",
                    "message": f"Server error: {str(e)}"
                }))
    
    except WebSocketDisconnect:
        print(f"💬 User {user_id} disconnected from chat")
    except Exception as e:
        print(f"❌ WebSocket connection error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Always close database session
        db.close()
        # Always remove from active connections
        if user_id in chat_manager.active_connections:
            del chat_manager.active_connections[user_id]
        print(f"💬 User {user_id} cleaned up")


# ==================== REST API ENDPOINTS ====================

@router.post("/send")
async def send_message_rest(
    request: SendMessageRequest,
    db: Session = Depends(get_db)
):
    """
    Send a message (REST API for mobile app compatibility)
    FIXED: Now accepts JSON body instead of query parameters
    """
    
    # Check if both users exist
    sender = db.query(Tenant).filter(Tenant.id == request.sender_id).first()
    receiver = db.query(Tenant).filter(Tenant.id == request.receiver_id).first()
    
    if not sender:
        raise HTTPException(status_code=404, detail="Sender not found")
    if not receiver:
        raise HTTPException(status_code=404, detail="Receiver not found")
    
    # Create message in database
    chat_message = ChatMessage(
        sender_id=request.sender_id,
        receiver_id=request.receiver_id,
        text=request.message,
        message_type=request.message_type,
        media_url=request.media_url,
        timestamp=datetime.utcnow()
    )
    db.add(chat_message)
    db.commit()
    db.refresh(chat_message)
    
    print(f"✅ Message saved: {sender.name} -> {receiver.name}: '{request.message}'")
    
    return {
        "status": "success",
        "message_id": chat_message.id,
        "timestamp": chat_message.timestamp.isoformat(),
        "sender": {
            "id": sender.id,
            "name": sender.name
        },
        "receiver": {
            "id": receiver.id,
            "name": receiver.name
        }
    }


@router.get("/health")
async def chat_health():
    """Health check for chat system"""
    return {
        "status": "healthy",
        "service": "chat_v3",
        "websocket": "ready",
        "rest_api": "ready"
    }
