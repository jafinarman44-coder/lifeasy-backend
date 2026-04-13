"""
Quick Migration Script for LIFEASY V27 PostgreSQL
Adds missing columns: is_verified, is_active, profile_photo
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("❌ ERROR: DATABASE_URL not found in .env file!")
    exit(1)

print("🔧 Starting database migration...")
print(f"📡 Database: {DATABASE_URL.split('@')[-1] if '@' in DATABASE_URL else 'Local'}")

try:
    # Create engine
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        print("\n✅ Connected to PostgreSQL database")
        
        # Check current columns
        print("\n🔍 Checking current table structure...")
        result = conn.execute(text("""
            SELECT column_name, data_type 
            FROM information_schema.columns 
            WHERE table_name = 'tenants'
            ORDER BY ordinal_position
        """))
        columns = {row[0]: row[1] for row in result}
        
        print(f"📋 Found {len(columns)} columns:")
        for col, dtype in columns.items():
            print(f"   - {col}: {dtype}")
        
        # Add is_verified if missing
        if 'is_verified' not in columns:
            print("\n➕ Adding is_verified column...")
            conn.execute(text("ALTER TABLE tenants ADD COLUMN is_verified BOOLEAN DEFAULT FALSE"))
            conn.commit()
            print("✅ is_verified column added")
        else:
            print("\n✅ is_verified column already exists")
        
        # Add is_active if missing
        if 'is_active' not in columns:
            print("➕ Adding is_active column...")
            conn.execute(text("ALTER TABLE tenants ADD COLUMN is_active BOOLEAN DEFAULT FALSE"))
            conn.commit()
            print("✅ is_active column added")
        else:
            print("✅ is_active column already exists")
        
        # Add profile_photo if missing
        if 'profile_photo' not in columns:
            print("➕ Adding profile_photo column...")
            conn.execute(text("ALTER TABLE tenants ADD COLUMN profile_photo TEXT"))
            conn.commit()
            print("✅ profile_photo column added")
        else:
            print("✅ profile_photo column already exists")
        
        # Update existing tenants
        print("\n🔄 Updating existing tenant records...")
        result = conn.execute(text("""
            UPDATE tenants 
            SET is_verified = TRUE, is_active = TRUE 
            WHERE is_verified IS NULL OR is_active IS NULL
        """))
        conn.commit()
        print(f"✅ Updated {result.rowcount} tenant(s)")
        
        # Verify final structure
        print("\n📊 Final verification:")
        result = conn.execute(text("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = 'tenants'
            AND column_name IN ('is_verified', 'is_active', 'profile_photo')
            ORDER BY column_name
        """))
        
        print("\n✅ Migration complete! New columns:")
        for row in result:
            print(f"   - {row[0]}: {row[1]} (nullable: {row[2]}, default: {row[3]})")
        
        # Count tenants
        result = conn.execute(text("SELECT COUNT(*) FROM tenants"))
        count = result.scalar()
        print(f"\n📈 Total tenants in database: {count}")
        
        conn.close()
        print("\n🎉 Migration completed successfully!")
        
except Exception as e:
    print(f"\n❌ Migration failed: {str(e)}")
    import traceback
    traceback.print_exc()
    exit(1)
