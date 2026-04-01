-- ============================================
-- LIFEASY V27+ PHASE 6 STEP 10
-- REAL-TIME CHAT SYSTEM - SQL MIGRATION
-- ============================================

-- This migration adds complete chat functionality
-- Compatible with existing tables (backward compatible)

-- ============================================
-- 1. CHAT PRESENCE TABLE (Online/Offline Tracking)
-- ============================================

CREATE TABLE IF NOT EXISTS chat_presence (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL UNIQUE,
    status TEXT DEFAULT 'offline',  -- 'online', 'offline', 'away'
    last_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
    building_id INTEGER,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Index for fast lookups
CREATE INDEX IF NOT EXISTS idx_presence_user ON chat_presence(user_id);
CREATE INDEX IF NOT EXISTS idx_presence_status ON chat_presence(status);
CREATE INDEX IF NOT EXISTS idx_presence_building ON chat_presence(building_id);


-- ============================================
-- 2. CHAT TYPING INDICATOR TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS chat_typing (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    room_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    is_typing BOOLEAN DEFAULT FALSE,
    started_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    expires_at DATETIME,
    UNIQUE(room_id, user_id)
);

CREATE INDEX IF NOT EXISTS idx_typing_room ON chat_typing(room_id);
CREATE INDEX IF NOT EXISTS idx_typing_user ON chat_typing(user_id);


-- ============================================
-- 3. ENHANCED CHAT_MESSAGES TABLE
-- Already exists, adding new columns
-- ============================================

-- Add new columns to existing chat_messages table
ALTER TABLE chat_messages ADD COLUMN room_id INTEGER;
ALTER TABLE chat_messages ADD COLUMN message_type TEXT DEFAULT 'text';  -- text, image, video, file
ALTER TABLE chat_messages ADD COLUMN media_url TEXT;  -- URL/path for media files
ALTER TABLE chat_messages ADD COLUMN deleted_by_sender BOOLEAN DEFAULT FALSE;
ALTER TABLE chat_messages ADD COLUMN deleted_by_receiver BOOLEAN DEFAULT FALSE;
ALTER TABLE chat_messages ADD COLUMN edited_at DATETIME;

-- Add foreign key constraint
ALTER TABLE chat_messages ADD CONSTRAINT fk_room FOREIGN KEY (room_id) REFERENCES chat_rooms(id);


-- ============================================
-- 4. CHAT UNREAD COUNTERS TABLE
-- ============================================

CREATE TABLE IF NOT EXISTS chat_unread (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,
    unread_count INTEGER DEFAULT 0,
    last_read_message_id INTEGER,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, room_id)
);

CREATE INDEX IF NOT EXISTS idx_unread_user ON chat_unread(user_id);
CREATE INDEX IF NOT EXISTS idx_unread_room ON chat_unread(room_id);


-- ============================================
-- 5. ENHANCED BLOCKED_USERS TABLE
-- Already exists, ensure unique constraints
-- ============================================

-- Ensure unique block relationships (already in models.py)
CREATE UNIQUE INDEX IF NOT EXISTS idx_block_unique 
ON blocked_users(blocker_id, blocked_id);

-- Add timestamp for when block occurred
ALTER TABLE blocked_users ADD COLUMN blocked_at DATETIME DEFAULT CURRENT_TIMESTAMP;


-- ============================================
-- 6. CHAT ROOM METADATA
-- ============================================

-- Add metadata to existing chat_rooms table
ALTER TABLE chat_rooms ADD COLUMN name TEXT;  -- For group chats
ALTER TABLE chat_rooms ADD COLUMN created_by INTEGER;
ALTER TABLE chat_rooms ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP;
ALTER TABLE chat_rooms ADD COLUMN last_message_at DATETIME;
ALTER TABLE chat_rooms ADD COLUMN is_active BOOLEAN DEFAULT TRUE;


-- ============================================
-- 7. SEED DATA FOR TESTING
-- ============================================

-- Insert sample presence records (will be updated by real users)
INSERT OR IGNORE INTO chat_presence (user_id, status, building_id) 
VALUES (1, 'online', 1);

INSERT OR IGNORE INTO chat_presence (user_id, status, building_id) 
VALUES (2, 'offline', 1);


-- ============================================
-- 8. VIEWS FOR COMMON QUERIES
-- ============================================

-- View: Online users count per building
CREATE VIEW IF NOT EXISTS view_online_users AS
SELECT 
    building_id,
    COUNT(*) as online_count
FROM chat_presence
WHERE status = 'online'
GROUP BY building_id;

-- View: Unread messages per user
CREATE VIEW IF NOT EXISTS view_unread_counts AS
SELECT 
    u.user_id,
    SUM(u.unread_count) as total_unread
FROM chat_unread u
GROUP BY u.user_id;

-- View: Recent active chats
CREATE VIEW IF NOT EXISTS view_active_chats AS
SELECT 
    cr.id as room_id,
    cr.last_message_at,
    COUNT(DISTINCT cp.tenant_id) as participant_count
FROM chat_rooms cr
LEFT JOIN chat_participants cp ON cr.id = cp.room_id
WHERE cr.is_active = TRUE
GROUP BY cr.id
ORDER BY cr.last_message_at DESC
LIMIT 50;


-- ============================================
-- 9. TRIGGERS FOR AUTO-UPDATES
-- ============================================

-- Trigger: Update last_message_at when new message inserted
CREATE TRIGGER IF NOT EXISTS update_room_last_message
AFTER INSERT ON chat_messages
BEGIN
    UPDATE chat_rooms 
    SET last_message_at = NEW.timestamp
    WHERE id = NEW.room_id;
END;

-- Trigger: Clean up old typing indicators (auto-expire after 5 seconds)
CREATE TRIGGER IF NOT EXISTS cleanup_typing
AFTER UPDATE OF expires_at ON chat_typing
WHEN datetime('now') > NEW.expires_at
BEGIN
    DELETE FROM chat_typing WHERE id = NEW.id;
END;

-- Trigger: Auto-update timestamp on presence change
CREATE TRIGGER IF NOT EXISTS update_presence_timestamp
AFTER UPDATE ON chat_presence
BEGIN
    UPDATE chat_presence 
    SET updated_at = CURRENT_TIMESTAMP 
    WHERE id = NEW.id;
END;


-- ============================================
-- MIGRATION COMPLETE
-- ============================================

-- Verify migration
SELECT 'Migration Complete' as status;
SELECT 'Tables Created:' as info;
SELECT COUNT(*) as table_count 
FROM information_schema.tables 
WHERE table_schema = 'main' 
AND table_name LIKE 'chat_%';
