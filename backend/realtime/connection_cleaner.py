"""
LIFEASY V27 - Connection Cleaner
Background thread for cleaning stale connections
Runs every 30 seconds
"""
import time
import threading
from typing import Callable, Optional

class ConnectionCleaner:
    """
    Background cleaner for stale WebSocket connections
    Prevents resource leaks from dead connections
    """
    
    def __init__(
        self,
        check_interval: int = 30,
        stale_timeout: int = 45,
        cleanup_callback: Optional[Callable] = None
    ):
        self.check_interval = check_interval  # How often to check (seconds)
        self.stale_timeout = stale_timeout    # Max idle time before cleanup
        self.cleanup_callback = cleanup_callback
        
        self._running = False
        self._thread = None
        
    def start(self):
        """Start the cleaner background thread"""
        self._running = True
        self._thread = threading.Thread(
            target=self._cleanup_loop,
            daemon=True
        )
        self._thread.start()
        print(f"🧹 Connection cleaner started (interval: {self.check_interval}s, timeout: {self.stale_timeout}s)")
    
    def stop(self):
        """Stop the cleaner"""
        self._running = False
        if self._thread:
            self._thread.join(timeout=5)
        print("🧹 Connection cleaner stopped")
    
    def _cleanup_loop(self):
        """Main cleanup loop"""
        while self._running:
            try:
                if self.cleanup_callback:
                    cleaned = self.cleanup_callback(self.stale_timeout)
                    if cleaned:
                        print(f"🧹 Cleaned {cleaned} stale connections")
            except Exception as e:
                print(f"Error in cleanup loop: {e}")
            
            # Sleep for check_interval
            time.sleep(self.check_interval)


# Global instance (will be configured in main)
connection_cleaner = ConnectionCleaner()
