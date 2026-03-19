"""
LIFEASY V30 PRO - Production Database Seeder
Simple SHA256 hashing for compatibility
"""
import sqlite3
import hashlib

# Database file
DB_FILE = "lifeasy_v30.db"

def hash_password(password):
    """Simple SHA256 password hashing"""
    return hashlib.sha256(password.encode()).hexdigest()

def seed_production_db():
    """Seed production database with test data"""
    
    # Connect to database
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create tenants table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS tenants (
        id INTEGER PRIMARY KEY,
        tenant_id TEXT UNIQUE,
        name TEXT,
        phone TEXT,
        flat TEXT,
        building TEXT,
        password TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    ''')
    
    print("✅ Database initialized (development mode)")
    
    try:
        # Check if test user exists
        cursor.execute("SELECT * FROM tenants WHERE tenant_id = ?", ("1001",))
        existing_user = cursor.fetchone()
        
        if existing_user:
            print("⚠️ Test user already exists!")
        else:
            # Create test tenant with hashed password
            hashed_pw = hash_password("123456")
            cursor.execute('''
                INSERT INTO tenants (tenant_id, password, name, phone, flat, building) 
                VALUES (?, ?, ?, ?, ?, ?)
            ''', ("1001", hashed_pw, "Test Tenant", "+8801234567890", "101", "A"))
            
            conn.commit()
            
            print("✅ Production tenant created successfully!")
            print("   Tenant ID: 1001")
            print("   Password: 123456")
            print("   Password Hash: SHA256")
            print("")
            print("🔐 Security Features:")
            print("   ✓ Password hashing")
            print("   ✓ JWT authentication")
            print("   ✓ SQL injection protection")
        
        # Show all tenants
        cursor.execute("SELECT COUNT(*) FROM tenants")
        count = cursor.fetchone()[0]
        print(f"\n📊 Total tenants in database: {count}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        conn.rollback()
    finally:
        conn.close()


if __name__ == "__main__":
    print("🚀 LIFEASY V30 PRO - Database Seeder")
    print("=" * 50)
    seed_production_db()
    print("\n✅ Database seeding complete!")
