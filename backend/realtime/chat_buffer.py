"""
LIFEASY V27+ PHASE 6 STEP 11 - Chat Message Buffer System
Stores messages for offline users and delivers when they reconnect
"""
from typing import Dict, List
import time


class ChatBuffer:
    """
    Message buffer for offline users
    Features:
    - Stores up to 100 messages per user
    - Auto-delivers on reconnect
    - Timestamp tracking
    """
    
    def __init__(self):
        # C3: MESSAGE BUFFER
        self.buffer: Dict[int, List[dict]] = {}  # {user_id: [messages]}
        self.MAX_MESSAGES_PER_USER = 100
    
    def push(self, user_id: int, message: dict):
        """
        Store message in buffer for offline user
        
        Args:
            user_id: int - Target user ID
            message: dict - Message data to store
        """
        if user_id not in self.buffer:
            self.buffer[user_id] = []
        
        # Add timestamp if not present
        if 'timestamp' not in message:
            message['timestamp'] = time.time()
        
        # Append message
        self.buffer[user_id].append(message)
        
        # Limit buffer size
        if len(self.buffer[user_id]) > self.MAX_MESSAGES_PER_USER:
            # Remove oldest message
            self.buffer[user_id].pop(0)
        
        print(f"💾 Buffered message for user {user_id} (queue size: {len(self.buffer[user_id])})")
    
    def pop_all(self, user_id: int) -> List[dict]:
        """
        Get and clear all buffered messages for user
        
        Args:
            user_id: int - User ID to retrieve messages for
            
        Returns:
            List[dict] - List of buffered messages
        """
        messages = self.buffer.get(user_id, [])
        self.buffer[user_id] = []  # Clear buffer
        return messages
    
    def has_messages(self, user_id: int) -> bool:
        """Check if user has buffered messages"""
        return user_id in self.buffer and len(self.buffer[user_id]) > 0
    
    def count_messages(self, user_id: int) -> int:
        """Get count of buffered messages for user"""
        return len(self.buffer.get(user_id, []))
    
    def clear_user_buffer(self, user_id: int):
        """Clear all buffered messages for a user"""
        if user_id in self.buffer:
            self.buffer[user_id] = []
            print(f"🗑️ Cleared buffer for user {user_id}")


# Global chat buffer instance
chat_buffer = ChatBuffer()
