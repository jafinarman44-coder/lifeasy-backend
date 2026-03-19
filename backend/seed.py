"""
LIFEASY V28 ULTRA - Database Seeder
Creates test tenant for development and testing
"""
from sqlalchemy.orm import Session
from database import SessionLocal, Base, engine
from models import Tenant
from passlib.context import CryptContext

# Create tables first
print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("✓ Tables created")
print("")

pwd_context = CryptContext(schemes=["bcrypt"])

# Create database session
db = SessionLocal()

try:
    # Check if user already exists
    existing_user = db.query(Tenant).filter(Tenant.tenant_id == "1001").first()
    
    if existing_user:
        print("⚠️ Test user already exists!")
    else:
        # Create test tenant with hashed password
        user = Tenant(
            tenant_id="1001",
            password=pwd_context.hash("123456")
        )
        
        db.add(user)
        db.commit()
        print("✅ Test tenant created successfully!")
        print("   Tenant ID: 1001")
        print("   Password: 123456")
        print("   Password is securely hashed with bcrypt")
        
finally:
    db.close()

print("\n✅ Database seeding complete!")
