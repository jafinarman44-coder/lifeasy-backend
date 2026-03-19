"""Simple seed - no bcrypt (compatibility fix)"""
import sqlite3
import hashlib

# Database file
DB_FILE = "lifeasy_v30.db"

# Simple password hasher (SHA256 - for demo only)
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Connect to database
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Create tenants table
cursor.execute('''
CREATE TABLE IF NOT EXISTS tenants (
    id INTEGER PRIMARY KEY,
    tenant_id TEXT UNIQUE,
    password TEXT
)
''')

# Check if user exists
cursor.execute("SELECT * FROM tenants WHERE tenant_id = ?", ("1001",))
existing = cursor.fetchone()

if existing:
    print("⚠️ Test user already exists!")
else:
    # Insert test user with hashed password
    hashed_pw = hash_password("123456")
    cursor.execute(
        "INSERT INTO tenants (tenant_id, password) VALUES (?, ?)",
        ("1001", hashed_pw)
    )
    conn.commit()
    print("✅ Test tenant created successfully!")
    print("   Tenant ID: 1001")
    print("   Password: 123456")
    print("   Password is hashed with SHA256")

conn.close()
print("\n✅ Database seeding complete!")
print("\n📝 Note: Using SHA256 for demo. Use bcrypt in production.")
