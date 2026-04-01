"""
LIFEASY V27+ PHASE 6 - Database Migration Script
Safe migration with zero data loss
Adds new fields to existing tables and creates new tables
"""
import sqlite3
from datetime import datetime

DATABASE_PATH = "backend/lifeasy_v30.db"


def migrate_tenants_table():
    """Add new fields to tenants table"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    try:
        # Add email column (UNIQUE)
        cursor.execute("""
            ALTER TABLE tenants ADD COLUMN email TEXT UNIQUE
        """)
        print("✓ Added email column to tenants table")
        
        # Add password column (will be updated during OTP verification)
        cursor.execute("""
            ALTER TABLE tenants ADD COLUMN password TEXT
        """)
        print("✓ Added password column to tenants table")
        
        # Add is_verified column
        cursor.execute("""
            ALTER TABLE tenants ADD COLUMN is_verified BOOLEAN DEFAULT FALSE
        """)
        print("✓ Added is_verified column to tenants table")
        
        # Add is_active column
        cursor.execute("""
            ALTER TABLE tenants ADD COLUMN is_active BOOLEAN DEFAULT TRUE
        """)
        print("✓ Added is_active column to tenants table")
        
        # Add profile_photo column
        cursor.execute("""
            ALTER TABLE tenants ADD COLUMN profile_photo TEXT
        """)
        print("✓ Added profile_photo column to tenants table")
        
        conn.commit()
        print("✅ Tenants table migration completed successfully")
        
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print(f"⚠️  Column already exists: {e}")
        else:
            raise e
    finally:
        conn.close()


def create_otp_codes_table():
    """Create OTP codes table"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS otp_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            otp TEXT NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            is_used BOOLEAN DEFAULT FALSE
        )
    """)
    
    # Create index for faster lookups
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_otp_email ON otp_codes(email)
    """)
    
    conn.commit()
    conn.close()
    print("✅ OTP codes table created successfully")


def create_notifications_table():
    """Create notifications table"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tenant_id INTEGER,
            title TEXT NOT NULL,
            message TEXT NOT NULL,
            is_read BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create index for tenant-specific queries
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_notifications_tenant ON notifications(tenant_id)
    """)
    
    conn.commit()
    conn.close()
    print("✅ Notifications table created successfully")


def create_chat_system_tables():
    """Create chat system tables"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Chat rooms table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_rooms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            is_group BOOLEAN DEFAULT FALSE
        )
    """)
    print("✓ Created chat_rooms table")
    
    # Chat participants table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_participants (
            room_id INTEGER NOT NULL,
            tenant_id INTEGER NOT NULL,
            FOREIGN KEY (room_id) REFERENCES chat_rooms(id),
            FOREIGN KEY (tenant_id) REFERENCES tenants(id)
        )
    """)
    print("✓ Created chat_participants table")
    
    # Chat messages table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            room_id INTEGER NOT NULL,
            sender_id INTEGER NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (room_id) REFERENCES chat_rooms(id),
            FOREIGN KEY (sender_id) REFERENCES tenants(id)
        )
    """)
    print("✓ Created chat_messages table")
    
    # Blocked users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS blocked_users (
            blocker_id INTEGER NOT NULL,
            blocked_id INTEGER NOT NULL,
            FOREIGN KEY (blocker_id) REFERENCES tenants(id),
            FOREIGN KEY (blocked_id) REFERENCES tenants(id),
            UNIQUE(blocker_id, blocked_id)
        )
    """)
    print("✓ Created blocked_users table")
    
    # Create indexes
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_chat_participants_room ON chat_participants(room_id)
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_chat_messages_room ON chat_messages(room_id)
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_blocked_users ON blocked_users(blocker_id, blocked_id)
    """)
    
    conn.commit()
    conn.close()
    print("✅ Chat system tables created successfully")


def create_call_logs_table():
    """Create call logs table for tracking calls"""
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS call_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            caller_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            call_type TEXT NOT NULL,  -- 'audio' or 'video'
            status TEXT NOT NULL,     -- 'answered', 'missed', 'rejected'
            duration INTEGER DEFAULT 0,  -- in seconds
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (caller_id) REFERENCES tenants(id),
            FOREIGN KEY (receiver_id) REFERENCES tenants(id)
        )
    """)
    
    # Create indexes
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_call_logs_caller ON call_logs(caller_id)
    """)
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_call_logs_receiver ON call_logs(receiver_id)
    """)
    
    conn.commit()
    conn.close()
    print("✅ Call logs table created successfully")


def run_migration():
    """Run all migrations"""
    print("\n🚀 Starting Phase 6 Database Migration...\n")
    
    try:
        # Migrate existing tenants table
        migrate_tenants_table()
        
        # Create new tables
        create_otp_codes_table()
        create_notifications_table()
        create_chat_system_tables()
        create_call_logs_table()
        
        print("\n✅ Phase 6 Database Migration completed successfully!")
        print("📊 All tables updated without data loss\n")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        raise e


if __name__ == "__main__":
    run_migration()
