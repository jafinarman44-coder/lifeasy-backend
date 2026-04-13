"""
AUTO-APPROVE SPECIFIC USERS
Run this once to approve the two users who can't login
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.dirname(__file__))

from database_prod import SessionLocal, engine, Base
from models import Tenant

# Initialize database
Base.metadata.create_all(bind=engine)
db = SessionLocal()

print("\n" + "="*70)
print("AUTO-APPROVING USERS FOR LOGIN")
print("="*70)

# The two emails that need approval
emails = [
    'majadar1din@gmail.com',
    'sathiasabrin2211@gmail.com'
]

for email in emails:
    print(f"\nChecking: {email}")
    user = db.query(Tenant).filter(Tenant.email == email).first()
    
    if user:
        print(f"  ✓ User found")
        print(f"    Name: {user.name}")
        print(f"    ID: {user.id}")
        print(f"    Verified: {user.is_verified}")
        print(f"    Active: {user.is_active}")
        
        if not user.is_active:
            # Approve the user
            user.is_active = True
            
            # Auto-assign defaults if missing
            if not user.building:
                user.building = "Main Building"
            if not user.flat:
                user.flat = "1A"
            
            db.commit()
            print(f"  ✅ USER APPROVED!")
            print(f"    Building: {user.building}")
            print(f"    Flat: {user.flat}")
        else:
            print(f"  ✅ User already active - can login")
    else:
        print(f"  ✗ User not found in database")

# Check total approved users
print("\n" + "="*70)
print("ALL APPROVED USERS:")
print("="*70)

all_users = db.query(Tenant).filter(Tenant.is_active == True).all()
for user in all_users:
    print(f"  {user.id}. {user.email} - {user.name} (Active: {user.is_active})")

db.close()

print("\n" + "="*70)
print("✅ DONE! All users can now login!")
print("="*70 + "\n")
