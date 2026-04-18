"""
LIFEASY V27 - Message Buffer Queue
Queues messages for offline users and delivers on reconnect
"""
import json
import time
from typing import Dict, List
from collections import defaultdict
from threading import Lock

class MessageQueue:
    """
    Message queue for offline users
    Stores messages when recipient is offline
    Delivers on reconnect
    """
    
    def __init__(self):
        # user_id -> list of queued messages
        self._queues: Dict[int, List[dict]] = defaultdict(list)
        self._lock = Lock()
        
        # Max messages per user queue
        self.MAX_QUEUE_SIZE = 100
        self.MAX_AGE_SECONDS = 86400  # 24 hours
        
    def queue_message(self, user_id: int, message: dict):
        """
        Queue a message for offline user
        message should be a dict with all required fields
        """
        with self._lock:
            # Add timestamp
            message['queued_at'] = time.time()
            message['queued_at_iso'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
            
            # Add to queue
            self._queues[user_id].append(message)
            
            # Trim if exceeds max size (keep latest)
            if len(self._queues[user_id]) > self.MAX_QUEUE_SIZE:
                self._queues[user_id] = self._queues[user_id][-self.MAX_QUEUE_SIZE:]
            
            print(f"📬 Queued message for offline user {user_id} (queue size: {len(self._queues[user_id])})")
    
    def get_queued_messages(self, user_id: int) -> List[dict]:
        """
        Get and clear all queued messages for user
        Call this when user reconnects
        """
        with self._lock:
            messages = self._queues.pop(user_id, [])
            
            # Filter out old messages (> 24 hours)
            current_time = time.time()
            fresh_messages = [
                msg for msg in messages
                if current_time - msg.get('queued_at', 0) < self.MAX_AGE_SECONDS
            ]
            
            if fresh_messages:
                print(f"📤 Delivering {len(fresh_messages)} queued messages to user {user_id}")
            
            return fresh_messages
    
    def get_queue_size(self, user_id: int) -> int:
        """Get number of queued messages for user"""
        with self._lock:
            return len(self._queues.get(user_id, []))
    
    def clear_queue(self, user_id: int):
        """Clear all queued messages for user"""
        with self._lock:
            if user_id in self._queues:
                del self._queues[user_id]
    
    def cleanup_old_messages(self):
        """Remove messages older than MAX_AGE_SECONDS"""
        current_time = time.time()
        
        with self._lock:
            for user_id in list(self._queues.keys()):
                self._queues[user_id] = [
                    msg for msg in self._queues[user_id]
                    if current_time - msg.get('queued_at', 0) < self.MAX_AGE_SECONDS
                ]
                
                # Remove empty queues
                if not self._queues[user_id]:
                    del self._queues[user_id]
    
    def get_queue_stats(self) -> dict:
        """Get queue statistics"""
        with self._lock:
            total_messages = sum(len(q) for q in self._queues.values())
            total_users = len(self._queues)
            
            return {
                'total_queued_messages': total_messages,
                'users_with_messages': total_users,
                'queues': {
                    user_id: len(messages)
                    for user_id, messages in self._queues.items()
                }
            }
    
    def pop_all(self, user_id: int) -> List[dict]:
        """Alias for get_queued_messages - returns and clears all queued messages"""
        return self.get_queued_messages(user_id)
    
    def add_message(self, user_id: int, message: dict):
        """Alias for queue_message - adds message to queue"""
        self.queue_message(user_id, message)


# Global instance
message_queue = MessageQueue()
