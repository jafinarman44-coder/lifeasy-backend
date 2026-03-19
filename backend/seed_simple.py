"""Simple seed script for LIFEASY V30"""
import sqlite3
from passlib.context import CryptContext

# Database file
DB_FILE = "lifeasy_v30.db"

# Password hasher
pwd_context = CryptContext(schemes=["bcrypt"])

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
    # Insert test user
    hashed_pw = pwd_context.hash("123456")
    cursor.execute(
        "INSERT INTO tenants (tenant_id, password) VALUES (?, ?)",
        ("1001", hashed_pw)
    )
    conn.commit()
    print("✅ Test tenant created successfully!")
    print("   Tenant ID: 1001")
    print("   Password: 123456")
    print("   Password is securely hashed with bcrypt")

conn.close()
print("\n✅ Database seeding complete!")
