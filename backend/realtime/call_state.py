# ============================================
# THREAD SAFE CALL STATE
# prevents conflict from rapid call signals
# ============================================

import threading


class CallState:
    """
    Thread-safe call state management
    Features:
    - Prevents race conditions in call operations
    - Atomic call state updates
    - Safe concurrent access
    """
    
    def __init__(self):
        # caller → receiver mapping
        self.active_calls = {}
        # Thread lock for atomic operations
        self.lock = threading.Lock()
    
    def set_call(self, caller, receiver):
        """Set active call between caller and receiver"""
        with self.lock:
            self.active_calls[caller] = receiver
    
    def end_call(self, user_id):
        """End call for specified user"""
        with self.lock:
            if user_id in self.active_calls:
                del self.active_calls[user_id]
    
    def get_partner(self, user_id):
        """Get current call partner for user"""
        with self.lock:
            return self.active_calls.get(user_id)
    
    def is_in_call(self, user_id) -> bool:
        """Check if user is currently in a call"""
        with self.lock:
            return user_id in self.active_calls


# Global call state instance
call_state = CallState()
