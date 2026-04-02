from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from database_prod import get_db
from models_chat import ChatRoom, ChatMessage, ChatBlock
from datetime import datetime
import json

router = APIRouter(prefix="/api/chat/v2", tags=["Chat V2"])

connected_users = {}


@router.websocket("/ws/{user_id}")
async def chat_socket(ws: WebSocket, user_id: int, db: Session = Depends(get_db)):
    await ws.accept()
    connected_users[user_id] = ws

    try:
        while True:
            raw = await ws.receive_text()
            data = json.loads(raw)
            await handle_incoming_message(user_id, data, db)

    except WebSocketDisconnect:
        if user_id in connected_users:
            del connected_users[user_id]


def is_blocked(sender_id, receiver_id, db):
    """Check if sender is blocked by receiver"""
    block = db.query(ChatBlock).filter(
        ChatBlock.blocker_id == receiver_id,
        ChatBlock.blocked_id == sender_id
    ).first()

    return block is not None


async def handle_incoming_message(sender_id: int, data: dict, db: Session):
    """Handle incoming chat message"""
    # Extract message data
    receiver_id = data.get("receiver_id")
    content = data.get("content")
    message_type = data.get("message_type", "text")

    # Check if sender is blocked
    if is_blocked(sender_id, receiver_id, db):
        return {"status": "blocked", "message": "You are blocked by this user"}

    # TODO: Implement message saving logic
    # TODO: Implement message forwarding to receiver
    # TODO: Implement read receipts
