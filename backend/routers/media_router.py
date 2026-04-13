"""
LIFEASY V27 - Media Upload Router
Handles image, video, document, and voice message uploads
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from database_prod import get_db
from models import ChatMessage
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import os
import uuid
from pathlib import Path

router = APIRouter(prefix="/api/media", tags=["Media Upload"])

# Allowed file types
ALLOWED_IMAGE_TYPES = ["image/jpeg", "image/png", "image/gif", "image/webp"]
ALLOWED_VIDEO_TYPES = ["video/mp4", "video/quicktime", "video/webm"]
ALLOWED_DOCUMENT_TYPES = [
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "text/plain",
]

# Max file sizes (in bytes)
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_VIDEO_SIZE = 50 * 1024 * 1024  # 50MB
MAX_DOCUMENT_SIZE = 20 * 1024 * 1024  # 20MB

@router.post("/upload")
async def upload_media(
    file: UploadFile = File(...),
    sender_id: int = Form(...),
    receiver_id: Optional[int] = Form(None),
    room_id: Optional[int] = Form(None),
    db: Session = Depends(get_db)
):
    """
    Upload media file (image, video, document)
    Returns file path and message ID
    """
    
    # Validate file type
    if file.content_type not in (ALLOWED_IMAGE_TYPES + ALLOWED_VIDEO_TYPES + ALLOWED_DOCUMENT_TYPES):
        raise HTTPException(
            status_code=400,
            detail=f"File type {file.content_type} not allowed"
        )
    
    # Validate file size
    file_content = await file.read()
    file_size = len(file_content)
    
    if file.content_type in ALLOWED_IMAGE_TYPES and file_size > MAX_IMAGE_SIZE:
        raise HTTPException(status_code=400, detail="Image size must be less than 10MB")
    elif file.content_type in ALLOWED_VIDEO_TYPES and file_size > MAX_VIDEO_SIZE:
        raise HTTPException(status_code=400, detail="Video size must be less than 50MB")
    elif file.content_type in ALLOWED_DOCUMENT_TYPES and file_size > MAX_DOCUMENT_SIZE:
        raise HTTPException(status_code=400, detail="Document size must be less than 20MB")
    
    # Determine media type
    if file.content_type in ALLOWED_IMAGE_TYPES:
        message_type = "image"
        folder = "images"
    elif file.content_type in ALLOWED_VIDEO_TYPES:
        message_type = "video"
        folder = "videos"
    else:
        message_type = "document"
        folder = "documents"
    
    # Create upload directory
    upload_dir = f"media/{folder}"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate unique filename
    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = f"{upload_dir}/{unique_filename}"
    
    # Save file
    with open(file_path, "wb") as f:
        f.write(file_content)
    
    # Create chat message with media
    message = ChatMessage(
        sender_id=sender_id,
        receiver_id=receiver_id or 0,
        room_id=room_id,
        text=f"[{message_type}]" if message_type != "document" else file.filename,
        message_type=message_type,
        media_url=file_path
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    
    return {
        "success": True,
        "message_id": message.id,
        "message_type": message_type,
        "file_path": file_path,
        "file_name": file.filename,
        "file_size": file_size,
        "timestamp": message.timestamp.isoformat()
    }

@router.post("/upload-voice")
async def upload_voice_message(
    file: UploadFile = File(...),
    sender_id: int = Form(...),
    receiver_id: Optional[int] = Form(None),
    room_id: Optional[int] = Form(None),
    duration: int = Form(...),  # Duration in seconds
    db: Session = Depends(get_db)
):
    """
    Upload voice message (audio recording)
    """
    
    # Validate file type
    if file.content_type not in ["audio/mpeg", "audio/mp4", "audio/webm", "audio/ogg"]:
        raise HTTPException(status_code=400, detail="Invalid audio file type")
    
    # Validate file size (max 5 minutes = 300 seconds, ~5MB)
    file_content = await file.read()
    file_size = len(file_content)
    
    if file_size > 5 * 1024 * 1024:  # 5MB
        raise HTTPException(status_code=400, detail="Voice message must be less than 5MB")
    
    # Create upload directory
    upload_dir = "media/voice"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate unique filename
    file_extension = Path(file.filename).suffix
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = f"{upload_dir}/{unique_filename}"
    
    # Save file
    with open(file_path, "wb") as f:
        f.write(file_content)
    
    # Create chat message with voice
    message = ChatMessage(
        sender_id=sender_id,
        receiver_id=receiver_id or 0,
        room_id=room_id,
        text=f"[Voice message - {duration}s]",
        message_type="voice",
        media_url=file_path
    )
    db.add(message)
    db.commit()
    db.refresh(message)
    
    return {
        "success": True,
        "message_id": message.id,
        "message_type": "voice",
        "file_path": file_path,
        "duration": duration,
        "timestamp": message.timestamp.isoformat()
    }

@router.get("/view/{message_id}")
async def view_media(message_id: int, db: Session = Depends(get_db)):
    """
    Get media file information
    """
    message = db.query(ChatMessage).filter(ChatMessage.id == message_id).first()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found")
    
    if not message.media_url:
        raise HTTPException(status_code=404, detail="No media attached")
    
    if not os.path.exists(message.media_url):
        raise HTTPException(status_code=404, detail="Media file not found on server")
    
    # Get file size
    file_size = os.path.getsize(message.media_url)
    
    return {
        "success": True,
        "message_id": message.id,
        "message_type": message.message_type,
        "file_path": message.media_url,
        "file_size": file_size,
        "sender_id": message.sender_id,
        "timestamp": message.timestamp.isoformat()
    }

@router.delete("/delete/{message_id}")
async def delete_media(message_id: int, tenant_id: int, db: Session = Depends(get_db)):
    """
    Delete media message and file
    """
    message = db.query(ChatMessage).filter(
        ChatMessage.id == message_id,
        ChatMessage.sender_id == tenant_id
    ).first()
    
    if not message:
        raise HTTPException(status_code=404, detail="Message not found or unauthorized")
    
    # Delete file from disk
    if message.media_url and os.path.exists(message.media_url):
        os.remove(message.media_url)
    
    # Delete message from database
    db.delete(message)
    db.commit()
    
    return {
        "success": True,
        "message": "Media deleted successfully"
    }
