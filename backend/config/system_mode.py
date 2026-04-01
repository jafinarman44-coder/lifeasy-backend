# ============================================================
# SYSTEM MODE CONFIGURATION (Phase 6 Step 8 – Part E)
# ============================================================
# This file controls all system-wide stability features
# Configure once → applies to Backend + Mobile + Windows
# ============================================================

SYSTEM_MODE = {
    # =========================================
    # Q1: CALL STABILITY MODE
    # =========================================
    # Options: "whatsapp_stable" | "basic" | "advanced"
    # whatsapp_stable = Low latency, direct signaling only (RECOMMENDED)
    "call_mode": "whatsapp_stable",
    
    # =========================================
    # Q2: OFFLINE SYNC MODE
    # =========================================
    # True = Store & forward when user offline
    "offline_sync": True,
    
    # =========================================
    # Q3: HYBRID NOTIFICATION MODE
    # =========================================
    # True = FCM + WebSocket dual notifications
    "hybrid_notification": True,
    
    # =========================================
    # ADVANCED OPTIONS
    # =========================================
    
    # TURN Server (False = pure P2P, lower latency)
    "use_turn_server": False,
    
    # Message Buffer (Q2 component)
    "buffer_enabled": True,
    
    # Call Restore (auto-reconnect)
    "restore_enabled": True,
    
    # FCM Required for push notifications
    "fcm_required": True,
    
    # WebSocket Required for real-time
    "ws_required": True,
    
    # Rate Limiting
    "rate_limit_enabled": True,
    "rate_limit_max_calls": 10,  # per minute
    "rate_limit_window_seconds": 60,
    
    # Heartbeat Settings
    "heartbeat_interval_seconds": 15,
    "zombie_timeout_seconds": 35,
    
    # Call Queue
    "call_queue_enabled": True,
    
    # Message Expiry
    "message_expiry_seconds": 300,  # 5 minutes
}


def get_mode(key):
    """Get specific mode value"""
    return SYSTEM_MODE.get(key, False)


def is_whatsapp_stable():
    """Check if WhatsApp-stable mode is active"""
    return SYSTEM_MODE["call_mode"] == "whatsapp_stable"


def is_offline_sync_enabled():
    """Check if offline sync is enabled"""
    return SYSTEM_MODE["offline_sync"]


def is_hybrid_notification():
    """Check if hybrid notification is enabled"""
    return SYSTEM_MODE["hybrid_notification"]


def print_system_status():
    """Print current system configuration"""
    print("=" * 60)
    print("🔧 LIFEASY SYSTEM MODE CONFIGURATION")
    print("=" * 60)
    print(f"📞 Call Mode: {SYSTEM_MODE['call_mode']}")
    print(f"🔄 Offline Sync: {SYSTEM_MODE['offline_sync']}")
    print(f"🔔 Hybrid Notification: {SYSTEM_MODE['hybrid_notification']}")
    print(f"📦 Message Buffer: {SYSTEM_MODE['buffer_enabled']}")
    print(f"♻️ Auto Restore: {SYSTEM_MODE['restore_enabled']}")
    print(f"🌐 FCM Required: {SYSTEM_MODE['fcm_required']}")
    print(f"🔌 WS Required: {SYSTEM_MODE['ws_required']}")
    print(f"🛡️ Rate Limiting: {SYSTEM_MODE['rate_limit_enabled']} ({SYSTEM_MODE['rate_limit_max_calls']} calls/min)")
    print(f"💓 Heartbeat: {SYSTEM_MODE['heartbeat_interval_seconds']}s / Zombie: {SYSTEM_MODE['zombie_timeout_seconds']}s")
    print("=" * 60)
    print("✅ System configured for WhatsApp-level stability!")
    print("=" * 60)


# Print status on import
if __name__ == "__main__":
    print_system_status()
