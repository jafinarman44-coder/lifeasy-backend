"""
Add missing columns to otp_codes table
"""
import sqlite3

DB_PATH = "E:/SUNNY/Jewel/APPERTMENT SOFTWER/LIFEASY_V27/backend/lifeasy_v30.db"

print("="*60)
print("🔧 MIGRATING DATABASE")
print("="*60)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Check if columns exist
cursor.execute("PRAGMA table_info(otp_codes)")
columns = [row[1] for row in cursor.fetchall()]

print(f"\nCurrent columns: {columns}")

# Add missing columns
new_columns = ['name', 'phone', 'password']

for col in new_columns:
    if col not in columns:
        print(f"➕ Adding column: {col}")
        cursor.execute(f"ALTER TABLE otp_codes ADD COLUMN {col} TEXT")
        print(f"   ✅ {col} added successfully")
    else:
        print(f"   ⏭️  {col} already exists")

conn.commit()
conn.close()

print("\n" + "="*60)
print("✅ Migration complete!")
print("="*60)
