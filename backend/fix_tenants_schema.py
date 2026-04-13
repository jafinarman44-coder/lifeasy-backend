"""
Make tenant_id, flat, building nullable and phone nullable
"""
import sqlite3

DB_PATH = "E:/SUNNY/Jewel/APPERTMENT SOFTWER/LIFEASY_V27/backend/lifeasy_v30.db"

print("="*60)
print("🔧 FIXING TENANTS TABLE CONSTRAINTS")
print("="*60)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# SQLite doesn't support ALTER COLUMN, we need to recreate the table
print("\n⚠️  Recreating tenants table with updated schema...")

# Get existing data
cursor.execute("SELECT * FROM tenants")
existing_data = cursor.fetchall()
print(f"   Found {len(existing_data)} existing records")

# Drop old table
cursor.execute("DROP TABLE IF EXISTS tenants_backup")
cursor.execute("ALTER TABLE tenants RENAME TO tenants_old")

# Create new table
cursor.execute("""
CREATE TABLE tenants (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tenant_id VARCHAR UNIQUE,
    name VARCHAR NOT NULL,
    phone VARCHAR,
    flat VARCHAR,
    building VARCHAR,
    email VARCHAR UNIQUE,
    password VARCHAR,
    is_verified BOOLEAN DEFAULT 0,
    is_active BOOLEAN DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

print("   ✅ New table created")

# Migrate data
if existing_data:
    for row in existing_data:
        # Generate tenant_id if missing
        tenant_id = row[1] if row[1] else f"TENANT_{row[0]:04d}"
        cursor.execute("""
            INSERT INTO tenants 
            (id, tenant_id, name, phone, flat, building, email, password, is_verified, is_active, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (row[0], tenant_id, row[2], row[3], row[4], row[5], row[6], row[7], 
              row[8] if len(row) > 8 else 0, row[9] if len(row) > 9 else 0, row[10] if len(row) > 10 else None))

print(f"   ✅ Migrated {len(existing_data)} records")

# Drop old table
cursor.execute("DROP TABLE IF EXISTS tenants_old")

conn.commit()
conn.close()

print("\n" + "="*60)
print("✅ Schema update complete!")
print("="*60)
