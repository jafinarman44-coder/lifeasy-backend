"""
LIFEASY V27+ PHASE 6 STEP 4 - Voice/Video Call System
Handles call signaling and call logs
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database_prod import get_db
from models import CallLog, Tenant
from datetime import datetime
from typing import Optional

router = APIRouter(prefix="/api/chat/call", tags=["Call System"])


@router.post("/initiate")
def initiate_call(
    caller_id: int,
    receiver_id: int,
    call_type: str,  # 'voice' or 'video'
    db: Session = Depends(get_db)
):
    """Initiate a call (create call log entry)"""
    # Check if users exist
    caller = db.query(Tenant).filter(Tenant.id == caller_id).first()
    receiver = db.query(Tenant).filter(Tenant.id == receiver_id).first()
    
    if not caller or not receiver:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Create call log
    call_log = CallLog(
        caller_id=caller_id,
        receiver_id=receiver_id,
        call_type=call_type,
        status='initiated',
        started_at=datetime.utcnow()
    )
    db.add(call_log)
    db.commit()
    db.refresh(call_log)
    
    return {
        'status': 'success',
        'call_id': call_log.id,
        'message': f'{call_type.capitalize()} call initiated to user {receiver_id}'
    }


@router.post("/answer")
def answer_call(
    call_id: int,
    db: Session = Depends(get_db)
):
    """Answer an incoming call"""
    call_log = db.query(CallLog).filter(CallLog.id == call_id).first()
    
    if not call_log:
        raise HTTPException(status_code=404, detail="Call not found")
    
    # Update call status
    call_log.status = 'answered'
    call_log.answered_at = datetime.utcnow()
    db.commit()
    
    return {
        'status': 'success',
        'message': 'Call answered',
        'call_id': call_id
    }


@router.post("/end")
def end_call(
    call_id: int,
    duration_seconds: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """End an ongoing call"""
    call_log = db.query(CallLog).filter(CallLog.id == call_id).first()
    
    if not call_log:
        raise HTTPException(status_code=404, detail="Call not found")
    
    # Update call status
    call_log.status = 'ended'
    call_log.ended_at = datetime.utcnow()
    
    if duration_seconds:
        call_log.duration_seconds = duration_seconds
    
    db.commit()
    
    return {
        'status': 'success',
        'message': 'Call ended',
        'duration_seconds': duration_seconds
    }


@router.get("/history/{user_id}")
def get_call_history(user_id: int, limit: int = 50, db: Session = Depends(get_db)):
    """Get call history for a user"""
    calls = db.query(CallLog).filter(
        (CallLog.caller_id == user_id) | (CallLog.receiver_id == user_id)
    ).order_by(CallLog.started_at.desc()).limit(limit).all()
    
    return {
        'status': 'success',
        'count': len(calls),
        'calls': [
            {
                'id': call.id,
                'caller_id': call.caller_id,
                'receiver_id': call.receiver_id,
                'call_type': call.call_type,
                'status': call.status,
                'started_at': call.started_at.isoformat(),
                'duration_seconds': call.duration_seconds
            }
            for call in calls
        ]
    }


@router.get("/missed/{user_id}")
def get_missed_calls(user_id: int, db: Session = Depends(get_db)):
    """Get missed calls for a user"""
    missed = db.query(CallLog).filter(
        CallLog.receiver_id == user_id,
        CallLog.status == 'initiated'
    ).order_by(CallLog.started_at.desc()).all()
    
    return {
        'status': 'success',
        'count': len(missed),
        'missed_calls': [
            {
                'id': call.id,
                'caller_id': call.caller_id,
                'started_at': call.started_at.isoformat()
            }
            for call in missed
        ]
    }
