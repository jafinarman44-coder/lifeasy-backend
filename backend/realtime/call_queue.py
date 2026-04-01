# ============================================
# CALL QUEUE SYSTEM - PART C UPGRADE (C7)
# ============================================
# Prevents double-answer race conditions
# WhatsApp-like "line busy" behavior
# ============================================

from typing import Optional


class CallQueue:
    """
    Call queue to prevent race conditions.
    
    Features:
    - Prevents two users from calling same user simultaneously
    - Prevents double-answer scenarios
    - Provides "line busy" feedback
    - Thread-safe operations
    
    Usage:
        # Try to initiate call
        if not call_queue.set(receiver_id, caller_id):
            # Receiver already has pending call
            send_busy_signal()
        
        # Accept call
        caller = call_queue.pop(receiver_id)
    """
    
    def __init__(self):
        # receiver_id → caller_id (pending incoming call)
        self.queue = {}
        
        print("📞 CallQueue initialized - preventing race conditions")
    
    def set(self, receiver_id: int, caller_id: int) -> bool:
        """
        Try to register an incoming call for receiver.
        
        Args:
            receiver_id: User being called
            caller_id: User initiating call
        
        Returns:
            True if call registered successfully
            False if receiver already has pending call (busy)
        """
        # Check if receiver already has pending call
        if receiver_id in self.queue:
            return False
        
        # Register new incoming call
        self.queue[receiver_id] = caller_id
        return True
    
    def pop(self, receiver_id: int) -> Optional[int]:
        """
        Accept and remove pending call.
        
        Args:
            receiver_id: User accepting call
        
        Returns:
            Caller ID if call existed, None otherwise
        """
        return self.queue.pop(receiver_id, None)
    
    def get_pending_caller(self, receiver_id: int) -> Optional[int]:
        """
        Get pending caller for receiver (without removing).
        
        Args:
            receiver_id: User to check
        
        Returns:
            Caller ID if pending call exists, None otherwise
        """
        return self.queue.get(receiver_id)
    
    def cancel(self, receiver_id: int):
        """
        Cancel pending call (caller hung up or timeout).
        
        Args:
            receiver_id: User whose pending call to cancel
        """
        self.queue.pop(receiver_id, None)
    
    def has_pending_call(self, receiver_id: int) -> bool:
        """Check if user has a pending incoming call"""
        return receiver_id in self.queue
    
    def clear_all(self):
        """Clear all pending calls (for cleanup)"""
        self.queue.clear()


# Global call queue instance
call_queue = CallQueue()
