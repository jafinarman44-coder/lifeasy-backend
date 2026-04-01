# ============================================
# MESSAGE BUFFER - PART C UPGRADE (C4)
# ============================================
# WhatsApp-style delivery buffer for offline users
# Stores signaling messages and delivers on reconnect
# ============================================

from typing import Dict, List
import time


class MessageBuffer:
    """
    Message delivery buffer for offline users.
    
    Features:
    - Stores signaling messages when recipient is offline
    - Auto-delivers pending messages on reconnect
    - Prevents lost call offers/signals
    - WhatsApp-like reliability
    
    Usage:
        # Store message for offline user
        message_buffer.store(receiver_id, {"action": "call_offer", ...})
        
        # Retrieve and deliver on reconnect
        pending = message_buffer.retrieve(user_id)
        for msg in pending:
            await send_signal(user_id, msg)
    """
    
    def __init__(self):
        # receiver_id → list of messages
        self.buffer: Dict[int, List[dict]] = {}
        
        # Message expiry time (5 minutes)
        self.expiry_seconds = 300
        
        print("📦 MessageBuffer initialized")
    
    def store(self, receiver_id: int, message: dict):
        """
        Store message for offline user.
        
        Args:
            receiver_id: User ID to receive message
            message: Signaling message dict
        """
        # Add timestamp for expiry tracking
        message_with_time = {
            **message,
            "_timestamp": time.time()
        }
        
        # Append to receiver's queue
        if receiver_id not in self.buffer:
            self.buffer[receiver_id] = []
        
        self.buffer[receiver_id].append(message_with_time)
        
        # Cleanup old messages
        self._cleanup_expired(receiver_id)
        
        print(f"💾 Stored message for user {receiver_id} (queue size: {len(self.buffer[receiver_id])})")
    
    def retrieve(self, receiver_id: int) -> List[dict]:
        """
        Retrieve all pending messages for user.
        Clears the buffer for this user after retrieval.
        
        Args:
            receiver_id: User ID
        
        Returns:
            List of pending messages (without internal timestamps)
        """
        messages = self.buffer.get(receiver_id, [])
        
        # Remove internal timestamp from messages
        clean_messages = []
        for msg in messages:
            clean_msg = {k: v for k, v in msg.items() if not k.startswith('_')}
            clean_messages.append(clean_msg)
        
        # Clear buffer for this user
        self.buffer[receiver_id] = []
        
        if clean_messages:
            print(f"📤 Delivered {len(clean_messages)} pending messages to user {receiver_id}")
        
        return clean_messages
    
    def _cleanup_expired(self, receiver_id: int):
        """Remove expired messages for a user"""
        now = time.time()
        if receiver_id in self.buffer:
            self.buffer[receiver_id] = [
                msg for msg in self.buffer[receiver_id]
                if (now - msg.get('_timestamp', 0)) < self.expiry_seconds
            ]
    
    def cleanup_all_expired(self):
        """Cleanup expired messages for all users"""
        now = time.time()
        for receiver_id in list(self.buffer.keys()):
            self.buffer[receiver_id] = [
                msg for msg in self.buffer[receiver_id]
                if (now - msg.get('_timestamp', 0)) < self.expiry_seconds
            ]
            
            # Remove empty queues
            if not self.buffer[receiver_id]:
                del self.buffer[receiver_id]
    
    def has_pending(self, receiver_id: int) -> bool:
        """Check if user has pending messages"""
        return receiver_id in self.buffer and len(self.buffer[receiver_id]) > 0
    
    def get_queue_size(self, receiver_id: int) -> int:
        """Get number of pending messages for user"""
        return len(self.buffer.get(receiver_id, []))


# Global message buffer instance
message_buffer = MessageBuffer()
