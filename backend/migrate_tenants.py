"""
Add is_verified and is_active columns to tenants table
"""
import sqlite3

DB_PATH = "E:/SUNNY/Jewel/APPERTMENT SOFTWER/LIFEASY_V27/backend/lifeasy_v30.db"

print("="*60)
print("🔧 MIGRATING TENANTS TABLE")
print("="*60)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Check current columns
cursor.execute("PRAGMA table_info(tenants)")
columns = [row[1] for row in cursor.fetchall()]

print(f"\nCurrent columns: {columns}")

# Add missing columns
new_columns = ['is_verified', 'is_active']

for col in new_columns:
    if col not in columns:
        print(f"➕ Adding column: {col}")
        cursor.execute(f"ALTER TABLE tenants ADD COLUMN {col} BOOLEAN DEFAULT 0")
        print(f"   ✅ {col} added successfully")
    else:
        print(f"   ⏭️  {col} already exists")

conn.commit()
conn.close()

print("\n" + "="*60)
print("✅ Tenants table migration complete!")
print("="*60)
