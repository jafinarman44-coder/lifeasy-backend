"""
LIFEASY V30 PRO - Production Database Migration Script
Fixes missing tables and columns to match the expected schema
"""
import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, Column, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

# Load environment
load_dotenv()

# Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

print(f"\n{'='*80}")
print(f"{BLUE}LIFEASY V30 PRO - DATABASE MIGRATION{RESET}")
print(f"{'='*80}\n")

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def check_and_add_column(table_name, column_name, column_type, default_value=None):
    """Check if column exists, add it if missing"""
    with engine.connect() as conn:
        # Check if column exists
        result = conn.execute(text(f"""
            SELECT COUNT(*)
            FROM information_schema.columns
            WHERE table_name = '{table_name}'
            AND column_name = '{column_name}'
        """))
        
        exists = result.fetchone()[0] > 0
        
        if exists:
            print(f"   ✅ {column_name} already exists")
            return True
        else:
            try:
                # Add column
                if default_value is not None:
                    if isinstance(default_value, str):
                        conn.execute(text(f"""
                            ALTER TABLE {table_name}
                            ADD COLUMN {column_name} {column_type} DEFAULT '{default_value}'
                        """))
                    else:
                        conn.execute(text(f"""
                            ALTER TABLE {table_name}
                            ADD COLUMN {column_name} {column_type} DEFAULT {default_value}
                        """))
                else:
                    conn.execute(text(f"""
                        ALTER TABLE {table_name}
                        ADD COLUMN {column_name} {column_type}
                    """))
                
                conn.commit()
                print(f"   ✅ {column_name} added successfully")
                return True
            except Exception as e:
                print(f"   ❌ Failed to add {column_name}: {e}")
                return False

def check_and_create_table(table_name, columns_sql):
    """Create table if it doesn't exist"""
    with engine.connect() as conn:
        result = conn.execute(text(f"""
            SELECT COUNT(*)
            FROM information_schema.tables
            WHERE table_name = '{table_name}'
        """))
        
        exists = result.fetchone()[0] > 0
        
        if exists:
            print(f"   ✅ {table_name} already exists")
            return True
        else:
            try:
                conn.execute(text(f"""
                    CREATE TABLE {table_name} (
                        {columns_sql}
                    )
                """))
                conn.commit()
                print(f"   ✅ {table_name} created successfully")
                return True
            except Exception as e:
                print(f"   ❌ Failed to create {table_name}: {e}")
                return False

# ============================================
# STEP 1: Fix tenants table
# ============================================
print(f"\n{BLUE}[1/3] Fixing 'tenants' table...{RESET}")
print(f"{'-'*80}")

check_and_add_column("tenants", "full_name", "VARCHAR(255)")
check_and_add_column("tenants", "is_approved", "BOOLEAN", False)
check_and_add_column("tenants", "updated_at", "TIMESTAMP")

# Copy data from 'name' to 'full_name' if needed
with engine.connect() as conn:
    try:
        result = conn.execute(text("""
            SELECT COUNT(*) FROM tenants WHERE full_name IS NULL AND name IS NOT NULL
        """))
        count = result.fetchone()[0]
        
        if count > 0:
            print(f"\n   📝 Copying data from 'name' to 'full_name' for {count} rows...")
            conn.execute(text("""
                UPDATE tenants
                SET full_name = name
                WHERE full_name IS NULL AND name IS NOT NULL
            """))
            conn.commit()
            print(f"   ✅ Data copied successfully")
    except Exception as e:
        print(f"   ⚠️  Could not copy data: {e}")

# ============================================
# STEP 2: Create missing tables
# ============================================
print(f"\n{BLUE}[2/3] Creating missing tables...{RESET}")
print(f"{'-'*80}")

# conversations table
check_and_create_table("conversations", """
    id SERIAL PRIMARY KEY,
    room_id VARCHAR(255) NOT NULL,
    tenant_id INTEGER NOT NULL,
    last_message TEXT,
    last_message_at TIMESTAMP,
    unread_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
""")

# settings table
check_and_create_table("settings", """
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL,
    key VARCHAR(255) NOT NULL,
    value TEXT,
    updated_at TIMESTAMP DEFAULT NOW()
""")

# Add more missing tables if needed
check_and_create_table("call_history", """
    id SERIAL PRIMARY KEY,
    caller_id INTEGER NOT NULL,
    receiver_id INTEGER NOT NULL,
    call_type VARCHAR(50),
    status VARCHAR(50),
    duration INTEGER,
    started_at TIMESTAMP,
    ended_at TIMESTAMP
""")

check_and_create_table("user_sessions", """
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER NOT NULL,
    token VARCHAR(500) NOT NULL,
    device_info TEXT,
    ip_address VARCHAR(50),
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP
""")

# ============================================
# STEP 3: Verify migration
# ============================================
print(f"\n{BLUE}[3/3] Verifying migration...{RESET}")
print(f"{'-'*80}")

with engine.connect() as conn:
    # Check tables
    result = conn.execute(text("""
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
        ORDER BY table_name
    """))
    tables = [row[0] for row in result.fetchall()]
    print(f"\n✅ Total tables: {len(tables)}")
    for table in tables:
        print(f"   ✅ {table}")
    
    # Check tenants schema
    print(f"\n📋 'tenants' table columns:")
    result = conn.execute(text("""
        SELECT column_name, data_type
        FROM information_schema.columns
        WHERE table_name = 'tenants'
        ORDER BY ordinal_position
    """))
    for row in result.fetchall():
        print(f"   ✅ {row[0]} ({row[1]})")
    
    # Check tenant data
    print(f"\n👥 Tenant data:")
    result = conn.execute(text("""
        SELECT id, full_name, name, email, is_approved
        FROM tenants
    """))
    for row in result.fetchall():
        print(f"   ID: {row[0]}, Full Name: {row[1]}, Name: {row[2]}, Email: {row[3]}, Approved: {row[4]}")

print(f"\n{'='*80}")
print(f"{GREEN}✅ DATABASE MIGRATION COMPLETED{RESET}")
print(f"{'='*80}\n")

print(f"{YELLOW}Next Steps:{RESET}")
print(f"1. Test API: python test_api_diagnostic.py")
print(f"2. Restart Render deployment")
print(f"3. Check Render logs for any errors\n")
