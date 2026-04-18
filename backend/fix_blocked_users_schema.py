"""
FIX BLOCKED_USERS TABLE SCHEMA
================================
Railway database has WRONG column names:
- user_id (WRONG)
- blocked_user_id (WRONG)

Code expects:
- blocker_id (CORRECT)
- blocked_id (CORRECT)

This script will:
1. Rename columns to match code expectations
2. Add missing indexes
3. Add blocked_at timestamp if missing
"""

import os
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

# Railway database connection
DATABASE_URL = os.environ.get('DATABASE_URL')

if not DATABASE_URL:
    print("❌ DATABASE_URL environment variable not set!")
    print("Please set it in Railway dashboard")
    exit(1)

def fix_blocked_users_table():
    """Fix the blocked_users table schema"""
    
    print("=" * 80)
    print("FIXING BLOCKED_USERS TABLE SCHEMA")
    print("=" * 80)
    
    try:
        # Connect to database
        print("\n🔗 Connecting to Railway database...")
        conn = psycopg2.connect(DATABASE_URL)
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()
        print("✅ Connected!")
        
        # Step 1: Check current columns
        print("\n📋 Checking current schema...")
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'blocked_users'
            ORDER BY ordinal_position
        """)
        columns = cursor.fetchall()
        
        print("\nCurrent columns:")
        for col in columns:
            print(f"  - {col[0]}: {col[1]}")
        
        # Step 2: Rename columns if needed
        print("\n🔧 Renaming columns...")
        
        # Check if old columns exist
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'blocked_users' 
            AND column_name IN ('user_id', 'blocked_user_id')
        """)
        old_columns = [row[0] for row in cursor.fetchall()]
        
        if 'user_id' in old_columns:
            print("  ✏️ Renaming 'user_id' → 'blocker_id'...")
            cursor.execute("""
                ALTER TABLE blocked_users 
                RENAME COLUMN user_id TO blocker_id
            """)
            print("  ✅ Renamed!")
        
        if 'blocked_user_id' in old_columns:
            print("  ✏️ Renaming 'blocked_user_id' → 'blocked_id'...")
            cursor.execute("""
                ALTER TABLE blocked_users 
                RENAME COLUMN blocked_user_id TO blocked_id
            """)
            print("  ✅ Renamed!")
        
        if not old_columns:
            print("  ✅ Columns already have correct names!")
        
        # Step 3: Add blocked_at if missing
        print("\n📅 Checking for blocked_at column...")
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'blocked_users' 
            AND column_name = 'blocked_at'
        """)
        
        if not cursor.fetchone():
            print("  ➕ Adding blocked_at column...")
            cursor.execute("""
                ALTER TABLE blocked_users 
                ADD COLUMN blocked_at TIMESTAMP DEFAULT NOW()
            """)
            print("  ✅ Added!")
        else:
            print("  ✅ blocked_at already exists!")
        
        # Step 4: Create/recreate indexes
        print("\n📊 Creating indexes...")
        
        cursor.execute("DROP INDEX IF EXISTS idx_blocked_blocker_id")
        cursor.execute("""
            CREATE INDEX idx_blocked_blocker_id 
            ON blocked_users(blocker_id)
        """)
        print("  ✅ idx_blocked_blocker_id created")
        
        cursor.execute("DROP INDEX IF EXISTS idx_blocked_blocked_id")
        cursor.execute("""
            CREATE INDEX idx_blocked_blocked_id 
            ON blocked_users(blocked_id)
        """)
        print("  ✅ idx_blocked_blocked_id created")
        
        cursor.execute("DROP INDEX IF EXISTS idx_blocked_unique")
        cursor.execute("""
            CREATE UNIQUE INDEX idx_blocked_unique 
            ON blocked_users(blocker_id, blocked_id)
        """)
        print("  ✅ idx_blocked_unique created")
        
        # Step 5: Add foreign key constraints if missing
        print("\n🔗 Checking foreign key constraints...")
        
        cursor.execute("""
            SELECT conname 
            FROM pg_constraint 
            WHERE conrelid = 'blocked_users'::regclass 
            AND contype = 'f'
        """)
        existing_fks = [row[0] for row in cursor.fetchall()]
        
        if 'blocked_users_blocker_id_fkey' not in existing_fks:
            print("  ➕ Adding FK: blocker_id → tenants.id...")
            cursor.execute("""
                ALTER TABLE blocked_users 
                ADD CONSTRAINT blocked_users_blocker_id_fkey 
                FOREIGN KEY (blocker_id) REFERENCES tenants(id) 
                ON DELETE CASCADE
            """)
            print("  ✅ Added!")
        
        if 'blocked_users_blocked_id_fkey' not in existing_fks:
            print("  ➕ Adding FK: blocked_id → tenants.id...")
            cursor.execute("""
                ALTER TABLE blocked_users 
                ADD CONSTRAINT blocked_users_blocked_id_fkey 
                FOREIGN KEY (blocked_id) REFERENCES tenants(id) 
                ON DELETE CASCADE
            """)
            print("  ✅ Added!")
        
        # Step 6: Verify final schema
        print("\n✅ Final schema verification...")
        cursor.execute("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'blocked_users'
            ORDER BY ordinal_position
        """)
        final_columns = cursor.fetchall()
        
        print("\nFinal columns:")
        for col in final_columns:
            print(f"  ✅ {col[0]}: {col[1]}")
        
        # Step 7: Test query
        print("\n🧪 Testing query...")
        cursor.execute("""
            SELECT COUNT(*) FROM blocked_users
        """)
        count = cursor.fetchone()[0]
        print(f"  ✅ Query successful! Found {count} blocked user records")
        
        print("\n" + "=" * 80)
        print("✅ BLOCKED_USERS TABLE SCHEMA FIXED SUCCESSFULLY!")
        print("=" * 80)
        print("\nWhat was fixed:")
        print("  ✅ user_id → blocker_id (renamed)")
        print("  ✅ blocked_user_id → blocked_id (renamed)")
        print("  ✅ blocked_at column added (if missing)")
        print("  ✅ Indexes created")
        print("  ✅ Foreign key constraints added")
        print("\nYour block/unblock features should now work!")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)

if __name__ == "__main__":
    fix_blocked_users_table()
