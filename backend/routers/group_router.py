"""
LIFEASY V27 - Group Chat & Group Call Router
Complete group management system
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from sqlalchemy import or_
from database_prod import get_db
from models import ChatRoom, ChatParticipant, ChatMessage, Tenant, GroupCallLog
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import os
import json
from realtime.group_chat_manager import group_chat_manager

router = APIRouter(prefix="/api/groups", tags=["Group Chat & Calls"])

# Pydantic schemas
class CreateGroupRequest(BaseModel):
    name: str
    description: Optional[str] = None
    member_ids: List[int]  # List of tenant IDs to add
    creator_id: int

class UpdateGroupRequest(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    group_photo: Optional[str] = None

class AddMemberRequest(BaseModel):
    tenant_ids: List[int]
    added_by: int

class RemoveMemberRequest(BaseModel):
    tenant_id: int
    removed_by: int

@router.post("/create")
async def create_group(request: CreateGroupRequest, db: Session = Depends(get_db)):
    """Create a new group chat"""
    
    # Validate creator
    creator = db.query(Tenant).filter(Tenant.id == request.creator_id).first()
    if not creator:
        raise HTTPException(status_code=404, detail="Creator not found")
    
    # Create group
    group = ChatRoom(
        is_group=True,
        group_name=request.name,
        group_description=request.description,
        created_by=request.creator_id
    )
    db.add(group)
    db.commit()
    db.refresh(group)
    
    # Add creator as admin
    creator_member = ChatParticipant(
        room_id=group.id,
        tenant_id=request.creator_id,
        is_admin=True
    )
    db.add(creator_member)
    
    # Add other members
    for member_id in request.member_ids:
        if member_id != request.creator_id:  # Skip creator (already added)
            tenant = db.query(Tenant).filter(Tenant.id == member_id).first()
            if tenant:
                member = ChatParticipant(
                    room_id=group.id,
                    tenant_id=member_id,
                    is_admin=False
                )
                db.add(member)
    
    db.commit()
    
    return {
        "success": True,
        "group_id": group.id,
        "message": "Group created successfully"
    }

@router.get("/list/{tenant_id}")
async def get_user_groups(tenant_id: int, db: Session = Depends(get_db)):
    """Get all groups user is member of"""
    
    # Get all rooms user is participant in
    participations = db.query(ChatParticipant).filter(
        ChatParticipant.tenant_id == tenant_id
    ).all()
    
    room_ids = [p.room_id for p in participations]
    
    # Filter for groups only
    groups = db.query(ChatRoom).filter(
        ChatRoom.id.in_(room_ids),
        ChatRoom.is_group == True
    ).all()
    
    result = []
    for group in groups:
        # Get member count
        member_count = db.query(ChatParticipant).filter(
            ChatParticipant.room_id == group.id
        ).count()
        
        # Get last message
        last_message = db.query(ChatMessage).filter(
            ChatMessage.room_id == group.id
        ).order_by(ChatMessage.timestamp.desc()).first()
        
        # Get creator name
        creator = db.query(Tenant).filter(Tenant.id == group.created_by).first()
        
        result.append({
            "id": group.id,
            "name": group.group_name,
            "description": group.group_description,
            "group_photo": group.group_photo,
            "created_by": creator.name if creator else "Unknown",
            "member_count": member_count,
            "last_message": last_message.text if last_message else None,
            "last_message_time": last_message.timestamp.isoformat() if last_message else None,
            "created_at": group.created_at.isoformat()
        })
    
    return {
        "success": True,
        "groups": result,
        "count": len(result)
    }

@router.get("/{group_id}")
async def get_group_info(group_id: int, db: Session = Depends(get_db)):
    """Get group details"""
    
    group = db.query(ChatRoom).filter(ChatRoom.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    # Get members
    members = db.query(ChatParticipant).filter(
        ChatParticipant.room_id == group_id
    ).all()
    
    member_list = []
    for member in members:
        tenant = db.query(Tenant).filter(Tenant.id == member.tenant_id).first()
        if tenant:
            member_list.append({
                "id": tenant.id,
                "name": tenant.name,
                "email": tenant.email,
                "is_admin": member.is_admin,
                "joined_at": member.joined_at.isoformat()
            })
    
    return {
        "success": True,
        "group": {
            "id": group.id,
            "name": group.group_name,
            "description": group.group_description,
            "group_photo": group.group_photo,
            "created_by": group.created_by,
            "created_at": group.created_at.isoformat()
        },
        "members": member_list,
        "member_count": len(member_list)
    }

@router.put("/update/{group_id}")
async def update_group(group_id: int, request: UpdateGroupRequest, db: Session = Depends(get_db)):
    """Update group information"""
    
    group = db.query(ChatRoom).filter(ChatRoom.id == group_id).first()
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    
    if request.name:
        group.group_name = request.name
    if request.description is not None:
        group.group_description = request.description
    if request.group_photo:
        group.group_photo = request.group_photo
    
    db.commit()
    
    return {
        "success": True,
        "message": "Group updated successfully"
    }

@router.post("/add-members/{group_id}")
async def add_members(group_id: int, request: AddMemberRequest, db: Session = Depends(get_db)):
    """Add members to group (admin only)"""
    
    # Verify requester is admin
    admin = db.query(ChatParticipant).filter(
        ChatParticipant.room_id == group_id,
        ChatParticipant.tenant_id == request.added_by,
        ChatParticipant.is_admin == True
    ).first()
    
    if not admin:
        raise HTTPException(status_code=403, detail="Only admins can add members")
    
    added_count = 0
    for tenant_id in request.tenant_ids:
        # Check if already member
        existing = db.query(ChatParticipant).filter(
            ChatParticipant.room_id == group_id,
            ChatParticipant.tenant_id == tenant_id
        ).first()
        
        if not existing:
            tenant = db.query(Tenant).filter(Tenant.id == tenant_id).first()
            if tenant:
                member = ChatParticipant(
                    room_id=group_id,
                    tenant_id=tenant_id,
                    is_admin=False
                )
                db.add(member)
                added_count += 1
    
    db.commit()
    
    return {
        "success": True,
        "message": f"Added {added_count} members to group",
        "added_count": added_count
    }

@router.post("/remove-member/{group_id}")
async def remove_member(group_id: int, request: RemoveMemberRequest, db: Session = Depends(get_db)):
    """Remove member from group (admin only)"""
    
    # Verify requester is admin
    admin = db.query(ChatParticipant).filter(
        ChatParticipant.room_id == group_id,
        ChatParticipant.tenant_id == request.removed_by,
        ChatParticipant.is_admin == True
    ).first()
    
    if not admin:
        raise HTTPException(status_code=403, detail="Only admins can remove members")
    
    # Cannot remove self
    if request.tenant_id == request.removed_by:
        raise HTTPException(status_code=400, detail="Cannot remove yourself. Use leave group instead.")
    
    member = db.query(ChatParticipant).filter(
        ChatParticipant.room_id == group_id,
        ChatParticipant.tenant_id == request.tenant_id
    ).first()
    
    if not member:
        raise HTTPException(status_code=404, detail="Member not found in group")
    
    db.delete(member)
    db.commit()
    
    return {
        "success": True,
        "message": "Member removed successfully"
    }

@router.post("/leave/{group_id}")
async def leave_group(group_id: int, tenant_id: int, db: Session = Depends(get_db)):
    """Leave a group"""
    
    member = db.query(ChatParticipant).filter(
        ChatParticipant.room_id == group_id,
        ChatParticipant.tenant_id == tenant_id
    ).first()
    
    if not member:
        raise HTTPException(status_code=404, detail="Not a member of this group")
    
    # If admin leaving, promote another or delete group
    if member.is_admin:
        # Check if other members exist
        other_members = db.query(ChatParticipant).filter(
            ChatParticipant.room_id == group_id,
            ChatParticipant.tenant_id != tenant_id
        ).all()
        
        if other_members:
            # Promote first member to admin
            other_members[0].is_admin = True
        else:
            # Delete group if last member leaving
            db.delete(member)
            db.query(ChatMessage).filter(ChatMessage.room_id == group_id).delete()
            db.query(ChatRoom).filter(ChatRoom.id == group_id).delete()
            db.commit()
            return {
                "success": True,
                "message": "Group deleted (you were the last member)"
            }
    
    db.delete(member)
    db.commit()
    
    return {
        "success": True,
        "message": "Left group successfully"
    }

@router.delete("/delete/{group_id}")
async def delete_group(group_id: int, tenant_id: int, db: Session = Depends(get_db)):
    """Delete group (admin only)"""
    
    admin = db.query(ChatParticipant).filter(
        ChatParticipant.room_id == group_id,
        ChatParticipant.tenant_id == tenant_id,
        ChatParticipant.is_admin == True
    ).first()
    
    if not admin:
        raise HTTPException(status_code=403, detail="Only admins can delete groups")
    
    # Delete all messages
    db.query(ChatMessage).filter(ChatMessage.room_id == group_id).delete()
    
    # Delete all participants
    db.query(ChatParticipant).filter(ChatParticipant.room_id == group_id).delete()
    
    # Delete group
    group = db.query(ChatRoom).filter(ChatRoom.id == group_id).first()
    db.delete(group)
    db.commit()
    
    return {
        "success": True,
        "message": "Group deleted successfully"
    }

@router.post("/upload-photo/{group_id}")
async def upload_group_photo(group_id: int, file: UploadFile = File(...)):
    """Upload group photo"""
    
    # Create uploads directory
    upload_dir = f"uploads/groups/{group_id}"
    os.makedirs(upload_dir, exist_ok=True)
    
    # Save file
    file_path = f"{upload_dir}/{file.filename}"
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    return {
        "success": True,
        "message": "Group photo uploaded successfully",
        "file_path": file_path
    }

@router.get("/members/{group_id}")
async def get_group_members(group_id: int, db: Session = Depends(get_db)):
    """Get all group members"""
    
    members = db.query(ChatParticipant).filter(
        ChatParticipant.room_id == group_id
    ).all()
    
    member_list = []
    for member in members:
        tenant = db.query(Tenant).filter(Tenant.id == member.tenant_id).first()
        if tenant:
            member_list.append({
                "id": tenant.id,
                "name": tenant.name,
                "email": tenant.email,
                "is_admin": member.is_admin,
                "joined_at": member.joined_at.isoformat()
            })
    
    return {
        "success": True,
        "members": member_list,
        "count": len(member_list)
    }


# ==================== WEBSOCKET ENDPOINT ====================

@router.websocket("/ws/{user_id}")
async def group_chat_websocket(ws: WebSocket, user_id: int, db: Session = Depends(get_db)):
    """
    WebSocket for real-time group chat
    Handles: messages, typing, calls, member events
    """
    # Get user's group rooms
    participations = db.query(ChatParticipant).filter(
        ChatParticipant.tenant_id == user_id
    ).all()
    
    room_ids = [p.room_id for p in participations]
    
    # Connect to group chat manager
    await group_chat_manager.connect(user_id, ws, room_ids)
    
    try:
        while True:
            # Wait for message
            raw = await ws.receive_text()
            data = json.loads(raw)
            action = data.get("action")
            
            # ==================== MESSAGE ACTIONS ====================
            
            if action == "send_group_message":
                room_id = data.get("room_id")
                text = data.get("text")
                message_type = data.get("message_type", "text")
                media_url = data.get("media_url")
                
                if not room_id or not text:
                    continue
                
                # Save message to database
                message = ChatMessage(
                    sender_id=user_id,
                    receiver_id=0,  # 0 for group messages
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
                    "id": message.id,
                    "sender_id": user_id,
                    "text": text,
                    "message_type": message_type,
                    "media_url": media_url,
                    "timestamp": message.timestamp.isoformat()
                }
                
                # Broadcast to group
                await group_chat_manager.send_group_message(
                    room_id=room_id,
                    sender_id=user_id,
                    message_data=message_data
                )
                
                # Confirm to sender
                await ws.send_text(json.dumps({
                    "action": "message_sent",
                    "message_id": message.id
                }))
            
            elif action == "typing_start" or action == "typing_stop":
                room_id = data.get("room_id")
                if room_id:
                    await group_chat_manager.broadcast_typing(
                        room_id=room_id,
                        user_id=user_id,
                        is_typing=(action == "typing_start")
                    )
            
            # ==================== CALL ACTIONS ====================
            
            elif action == "group_call_offer":
                room_id = data.get("room_id")
                call_data = data.get("call_data", {})
                
                await group_chat_manager.send_group_call_offer(
                    room_id=room_id,
                    caller_id=user_id,
                    call_data=call_data
                )
                
                # Log call
                call_log = GroupCallLog(
                    room_id=room_id,
                    caller_id=user_id,
                    call_type=call_data.get("call_type", "audio")
                )
                db.add(call_log)
                db.commit()
            
            elif action == "group_call_answer":
                room_id = data.get("room_id")
                answer_data = data.get("answer_data", {})
                
                await group_chat_manager.send_group_call_answer(
                    room_id=room_id,
                    responder_id=user_id,
                    answer_data=answer_data
                )
            
            elif action == "group_call_end":
                room_id = data.get("room_id")
                reason = data.get("reason", "ended")
                
                await group_chat_manager.send_group_call_end(
                    room_id=room_id,
                    user_id=user_id,
                    reason=reason
                )
                
                # Update call log
                call_log = db.query(GroupCallLog).filter(
                    GroupCallLog.room_id == room_id,
                    GroupCallLog.ended_at == None
                ).order_by(GroupCallLog.started_at.desc()).first()
                
                if call_log:
                    call_log.ended_at = datetime.utcnow()
                    duration = (call_log.ended_at - call_log.started_at).total_seconds()
                    call_log.duration = int(duration)
                    db.commit()
            
            elif action == "ping":
                await ws.send_text(json.dumps({"action": "pong"}))
    
    except WebSocketDisconnect:
        group_chat_manager.disconnect(user_id)
        print(f"👥 User {user_id} disconnected from group chat")
