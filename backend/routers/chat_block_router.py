"""
LIFEASY V27+ PHASE 6 STEP 4 - Block/Unblock System
Allows users to block/unblock other users
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database_prod import get_db
from models import BlockedUser, Tenant
from typing import List

router = APIRouter(prefix="/api/chat/block", tags=["Block System"])


@router.post("/add")
def add_block(
    user_id: int,
    target_id: int,
    db: Session = Depends(get_db)
):
    """Block a user"""
    # Check if already blocked
    existing = db.query(BlockedUser).filter(
        BlockedUser.blocker_id == user_id,
        BlockedUser.blocked_id == target_id
    ).first()
    
    if existing:
        return {
            'status': 'already_blocked',
            'message': 'User is already blocked'
        }
    
    # Create block record
    block = BlockedUser(blocker_id=user_id, blocked_id=target_id)
    db.add(block)
    db.commit()
    
    return {
        'status': 'success',
        'message': f'User {target_id} has been blocked'
    }


@router.post("/remove")
def remove_block(
    user_id: int,
    target_id: int,
    db: Session = Depends(get_db)
):
    """Unblock a user"""
    # Find and remove block
    block = db.query(BlockedUser).filter(
        BlockedUser.blocker_id == user_id,
        BlockedUser.blocked_id == target_id
    ).first()
    
    if not block:
        return {
            'status': 'not_found',
            'message': 'Block record not found'
        }
    
    db.delete(block)
    db.commit()
    
    return {
        'status': 'success',
        'message': f'User {target_id} has been unblocked'
    }


@router.get("/{user_id}")
def get_blocked_users(user_id: int, db: Session = Depends(get_db)):
    """Get list of blocked users"""
    blocks = db.query(BlockedUser).filter(
        BlockedUser.blocker_id == user_id
    ).all()
    
    blocked_ids = [block.blocked_id for block in blocks]
    
    # Get tenant details for blocked users
    blocked_users = []
    for bid in blocked_ids:
        tenant = db.query(Tenant).filter(Tenant.id == bid).first()
        if tenant:
            blocked_users.append({
                'id': tenant.id,
                'name': tenant.name,
                'email': tenant.email,
                'phone': tenant.phone
            })
    
    return {
        'status': 'success',
        'count': len(blocked_users),
        'blocked_users': blocked_users
    }


@router.get("/check/{user_id}/{target_id}")
def check_if_blocked(
    user_id: int,
    target_id: int,
    db: Session = Depends(get_db)
):
    """Check if user1 is blocked by user2"""
    block = db.query(BlockedUser).filter(
        BlockedUser.blocker_id == target_id,
        BlockedUser.blocked_id == user_id
    ).first()
    
    return {
        'status': 'success',
        'is_blocked': block is not None
    }
