# ============================================
# MESSAGE QUEUE FOR OFFLINE USERS
# Stores messages when user is unavailable
# ============================================


class MessageQueue:
    """
    Message buffering system for offline users
    Features:
    - Stores messages when user is offline
    - Delivers all messages on reconnect
    - Automatic cleanup after delivery
    """
    
    def __init__(self):
        # user_id → list of messages
        self.queues = {}
    
    def add_message(self, user_id: int, data: dict):
        """Add message to user's queue"""
        if user_id not in self.queues:
            self.queues[user_id] = []
        self.queues[user_id].append(data)
    
    def pop_all(self, user_id: int) -> list:
        """Get and clear all queued messages for user"""
        msgs = self.queues.get(user_id, [])
        if user_id in self.queues:
            del self.queues[user_id]
        return msgs
    
    def has_messages(self, user_id: int) -> bool:
        """Check if user has pending messages"""
        return user_id in self.queues and len(self.queues[user_id]) > 0
    
    def count_messages(self, user_id: int) -> int:
        """Get count of queued messages"""
        return len(self.queues.get(user_id, []))


# Global message queue instance
message_queue = MessageQueue()
