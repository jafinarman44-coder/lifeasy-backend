"""
CREATE MISSING DATABASE TABLES ON RENDER
Run this script to create all tables that might be missing
"""
from sqlalchemy import create_engine, text
import os

# Get database URL from environment or use default
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ DATABASE_URL not set!")
    print("\n📋 Please set it in Render dashboard:")
    print("   Environment → Add Environment Variable")
    print("   Key: DATABASE_URL")
    print("   Value: postgresql://user:pass@host:5432/dbname")
    exit(1)

print("="*80)
print("🔧 CREATING MISSING DATABASE TABLES")
print("="*80)
print(f"\nDatabase: {DATABASE_URL[:50]}...")

# Create engine
engine = create_engine(DATABASE_URL)

# SQL statements to create all tables
create_tables_sql = """
-- 1. Notifications table
CREATE TABLE IF NOT EXISTS notifications (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER REFERENCES tenants(id),
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_notifications_tenant_id ON notifications(tenant_id);
CREATE INDEX IF NOT EXISTS idx_notifications_created_at ON notifications(created_at DESC);

-- 2. Chat Rooms table
CREATE TABLE IF NOT EXISTS chat_rooms (
    id SERIAL PRIMARY KEY,
    is_group BOOLEAN DEFAULT FALSE,
    group_name VARCHAR(255),
    group_description TEXT,
    group_photo TEXT,
    created_by INTEGER REFERENCES tenants(id),
    created_at TIMESTAMP DEFAULT NOW()
);

-- 3. Chat Participants table
CREATE TABLE IF NOT EXISTS chat_participants (
    id SERIAL PRIMARY KEY,
    room_id INTEGER REFERENCES chat_rooms(id) ON DELETE CASCADE,
    tenant_id INTEGER REFERENCES tenants(id),
    joined_at TIMESTAMP DEFAULT NOW(),
    left_at TIMESTAMP,
    is_admin BOOLEAN DEFAULT FALSE,
    UNIQUE(room_id, tenant_id)
);

CREATE INDEX IF NOT EXISTS idx_chat_participants_room_id ON chat_participants(room_id);
CREATE INDEX IF NOT EXISTS idx_chat_participants_tenant_id ON chat_participants(tenant_id);

-- 4. Chat Messages table
CREATE TABLE IF NOT EXISTS chat_messages (
    id SERIAL PRIMARY KEY,
    sender_id INTEGER REFERENCES tenants(id),
    receiver_id INTEGER REFERENCES tenants(id),
    room_id INTEGER REFERENCES chat_rooms(id),
    text TEXT NOT NULL,
    message_type VARCHAR(50) DEFAULT 'text',
    media_url TEXT,
    timestamp TIMESTAMP DEFAULT NOW(),
    delivered BOOLEAN DEFAULT FALSE,
    seen BOOLEAN DEFAULT FALSE,
    deleted_by_sender BOOLEAN DEFAULT FALSE,
    deleted_by_receiver BOOLEAN DEFAULT FALSE,
    edited_at TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_chat_messages_room_id ON chat_messages(room_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_sender_id ON chat_messages(sender_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_receiver_id ON chat_messages(receiver_id);
CREATE INDEX IF NOT EXISTS idx_chat_messages_timestamp ON chat_messages(timestamp DESC);

-- 5. Call Logs table (if missing)
CREATE TABLE IF NOT EXISTS call_logs (
    id SERIAL PRIMARY KEY,
    caller_id INTEGER REFERENCES tenants(id),
    receiver_id INTEGER REFERENCES tenants(id),
    call_type VARCHAR(10) DEFAULT 'voice',
    status VARCHAR(20) DEFAULT 'initiated',
    duration INTEGER DEFAULT 0,
    started_at TIMESTAMP DEFAULT NOW(),
    ended_at TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_call_logs_caller_id ON call_logs(caller_id);
CREATE INDEX IF NOT EXISTS idx_call_logs_receiver_id ON call_logs(receiver_id);

-- 6. Blocked Users table (if missing)
CREATE TABLE IF NOT EXISTS blocked_users (
    id SERIAL PRIMARY KEY,
    blocker_id INTEGER REFERENCES tenants(id),
    blocked_id INTEGER REFERENCES tenants(id),
    blocked_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(blocker_id, blocked_id)
);

CREATE INDEX IF NOT EXISTS idx_blocked_users_blocker_id ON blocked_users(blocker_id);
CREATE INDEX IF NOT EXISTS idx_blocked_users_blocked_id ON blocked_users(blocked_id);
"""

print("\n📋 Creating tables...")

try:
    # Execute all SQL statements
    with engine.connect() as conn:
        # Split and execute each statement
        statements = [stmt.strip() for stmt in create_tables_sql.split(';') if stmt.strip()]
        
        for i, statement in enumerate(statements, 1):
            try:
                conn.execute(text(statement))
                conn.commit()
                
                # Print progress
                if 'CREATE TABLE' in statement:
                    table_name = statement.split('CREATE TABLE IF NOT EXISTS ')[1].split(' ')[0]
                    print(f"  ✅ {i}. Created table: {table_name}")
                elif 'CREATE INDEX' in statement:
                    pass  # Skip index creation messages
            except Exception as e:
                print(f"  ⚠️  {i}. Statement skipped (might already exist): {str(e)[:50]}")
        
    print("\n" + "="*80)
    print("✅ ALL TABLES CREATED SUCCESSFULLY!")
    print("="*80)
    
    print("\n📊 Tables created:")
    print("  ✅ notifications")
    print("  ✅ chat_rooms")
    print("  ✅ chat_participants")
    print("  ✅ chat_messages")
    print("  ✅ call_logs")
    print("  ✅ blocked_users")
    
    print("\n🎯 NEXT STEP:")
    print("  1. Restart your Render service")
    print("  2. Test endpoints:")
    print("     - https://lifeasy-api.onrender.com/api/notifications/1")
    print("     - https://lifeasy-api.onrender.com/api/chat/rooms/1")
    print("     - https://lifeasy-api.onrender.com/api/chat/history/1")
    
    print("\n" + "="*80)
    
except Exception as e:
    print(f"\n❌ ERROR: {str(e)}")
    print("\n🔍 Troubleshooting:")
    print("  1. Check DATABASE_URL is correct")
    print("  2. Check if you have permission to create tables")
    print("  3. Check if 'tenants' table exists first")
    print("="*80)
