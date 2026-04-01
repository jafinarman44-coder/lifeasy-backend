"""
LIFEASY V27+ PHASE 6 - Call Logs API
Track audio/video call history (signaling handled by client-side WebRTC)
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database_prod import get_db
from models import CallLog, Tenant
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

router = APIRouter(prefix="/api/calls", tags=["Calling"])


class StartCallRequest(BaseModel):
    caller_id: int
    receiver_id: int
    call_type: str  # 'audio' or 'video'


class EndCallRequest(BaseModel):
    call_id: int
    duration: int  # in seconds
    status: str  # 'answered', 'missed', 'rejected'


class CallLogResponse(BaseModel):
    id: int
    caller_id: int
    receiver_id: int
    call_type: str
    status: str
    duration: int
    created_at: datetime


@router.post("/start")
def start_call(data: StartCallRequest, db: Session = Depends(get_db)):
    """
    Log a new call attempt (for tracking purposes)
    Client handles WebRTC signaling separately
    """
    caller_id = data.caller_id
    receiver_id = data.receiver_id
    call_type = data.call_type
    
    # Verify users exist
    caller = db.query(Tenant).filter(Tenant.id == caller_id).first()
    receiver = db.query(Tenant).filter(Tenant.id == receiver_id).first()
    
    if not caller or not receiver:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "error", "message": "User not found"}
        )
    
    # Create call log entry (initially marked as missed/ongoing)
    call_log = CallLog(
        caller_id=caller_id,
        receiver_id=receiver_id,
        call_type=call_type,
        status="ongoing",
        duration=0
    )
    
    db.add(call_log)
    db.commit()
    db.refresh(call_log)
    
    return {
        "status": "success",
        "message": "Call started",
        "call_id": call_log.id,
        "data": {
            "caller": {
                "id": caller.id,
                "name": caller.name
            },
            "receiver": {
                "id": receiver.id,
                "name": receiver.name
            },
            "call_type": call_type
        }
    }


@router.post("/end")
def end_call(data: EndCallRequest, db: Session = Depends(get_db)):
    """
    Update call log with final status and duration
    """
    call_id = data.call_id
    duration = data.duration
    final_status = data.status
    
    # Find call log
    call_log = db.query(CallLog).filter(CallLog.id == call_id).first()
    
    if not call_log:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"status": "error", "message": "Call log not found"}
        )
    
    # Update call log
    call_log.status = final_status
    call_log.duration = duration
    
    db.commit()
    db.refresh(call_log)
    
    return {
        "status": "success",
        "message": "Call ended",
        "call_log": {
            "id": call_log.id,
            "caller_id": call_log.caller_id,
            "receiver_id": call_log.receiver_id,
            "call_type": call_log.call_type,
            "status": call_log.status,
            "duration": call_log.duration,
            "created_at": call_log.created_at.isoformat()
        }
    }


@router.get("/history/{tenant_id}")
def get_call_history(tenant_id: int, limit: int = 50, db: Session = Depends(get_db)):
    """
    Get call history for a tenant (both incoming and outgoing)
    """
    # Get calls where tenant is either caller or receiver
    call_logs = db.query(CallLog).filter(
        (CallLog.caller_id == tenant_id) | (CallLog.receiver_id == tenant_id)
    ).order_by(CallLog.created_at.desc()).limit(limit).all()
    
    return {
        "status": "success",
        "count": len(call_logs),
        "call_history": [
            {
                "id": call.id,
                "caller_id": call.caller_id,
                "receiver_id": call.receiver_id,
                "call_type": call.call_type,
                "status": call.status,
                "duration": call.duration,
                "created_at": call.created_at.isoformat(),
                "direction": "outgoing" if call.caller_id == tenant_id else "incoming"
            }
            for call in call_logs
        ]
    }


@router.get("/missed/{tenant_id}")
def get_missed_calls(tenant_id: int, db: Session = Depends(get_db)):
    """
    Get missed calls for a tenant
    """
    missed_calls = db.query(CallLog).filter(
        (CallLog.receiver_id == tenant_id) &
        (CallLog.status == "missed")
    ).order_by(CallLog.created_at.desc()).all()
    
    return {
        "status": "success",
        "count": len(missed_calls),
        "missed_calls": [
            {
                "id": call.id,
                "caller_id": call.caller_id,
                "receiver_id": call.receiver_id,
                "call_type": call.call_type,
                "created_at": call.created_at.isoformat()
            }
            for call in missed_calls
        ]
    }
