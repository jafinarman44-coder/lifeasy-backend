"""
LIFEASY V27+ PHASE 6 STEP 5 - Call Model
Pydantic model for call signaling
"""
from pydantic import BaseModel
from datetime import datetime


class CallSignal(BaseModel):
    """Call signaling message model"""
    action: str  # call_offer, call_answer, call_end, call_reject, ice-candidate
    caller: int
    receiver: int
    call_type: str  # 'voice' or 'video'
    timestamp: str = datetime.utcnow().isoformat()
    data: dict = {}  # Additional WebRTC data (SDP, ICE candidates, etc.)


class CallOffer(BaseModel):
    """Incoming call offer model"""
    action: str = "call_offer"
    caller: int
    caller_name: str
    caller_photo: str = None
    call_type: str  # 'voice' or 'video'
    timestamp: str = datetime.utcnow().isoformat()


class CallAnswer(BaseModel):
    """Call answer model"""
    action: str = "call_answer"
    receiver: int
    receiver_name: str
    timestamp: str = datetime.utcnow().isoformat()


class CallEnd(BaseModel):
    """Call end model"""
    action: str = "call_end"
    caller: int
    receiver: int
    duration: int  # in seconds
    timestamp: str = datetime.utcnow().isoformat()


class CallReject(BaseModel):
    """Call reject model"""
    action: str = "call_reject"
    receiver: int
    reason: str = "rejected"  # rejected, busy, unavailable
    timestamp: str = datetime.utcnow().isoformat()
