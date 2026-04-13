"""
QUICK FIX SCRIPT - Check and Approve Pending Users
Run this to check user status and approve them
"""
from database_prod import SessionLocal, engine, Base
from models import Tenant

# Initialize database
Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Check the two problematic users
emails_to_check = [
    'majadar1din@gmail.com',
    'sathiasabrin2211@gmail.com'
]

print("=" * 60)
print("CHECKING USER STATUS")
print("=" * 60)

for email in emails_to_check:
    user = db.query(Tenant).filter(Tenant.email == email).first()
    
    if user:
        print(f"\n✅ Email: {email}")
        print(f"   ID: {user.id}")
        print(f"   Name: {user.name}")
        print(f"   Phone: {user.phone}")
        print(f"   is_verified: {user.is_verified}")
        print(f"   is_active: {user.is_active}")
        print(f"   Created: {user.created_at}")
        
        if not user.is_active:
            print(f"\n   ⚠️  USER NOT APPROVED!")
            approve = input("   Approve this user now? (y/n): ").lower()
            
            if approve == 'y':
                user.is_active = True
                
                # Auto-assign building if missing
                if not user.building:
                    user.building = "Main Building"
                if not user.flat:
                    user.flat = "1A"
                
                db.commit()
                print(f"   ✅ User APPROVED successfully!")
                print(f"   Building: {user.building}")
                print(f"   Flat: {user.flat}")
            else:
                print(f"   ❌ User not approved")
        else:
            print(f"   ✅ User is ACTIVE and can login")
    else:
        print(f"\n❌ Email not found: {email}")

print("\n" + "=" * 60)
print("CHECKING ALL PENDING USERS")
print("=" * 60)

pending_users = db.query(Tenant).filter(
    Tenant.is_verified == True,
    Tenant.is_active == False
).all()

if pending_users:
    print(f"\nFound {len(pending_users)} pending users:\n")
    for user in pending_users:
        print(f"  {user.id}. {user.email} - {user.name} ({user.phone})")
    
    approve_all = input("\nApprove ALL pending users? (y/n): ").lower()
    
    if approve_all == 'y':
        for user in pending_users:
            user.is_active = True
            if not user.building:
                user.building = "Main Building"
            if not user.flat:
                user.flat = "1A"
        
        db.commit()
        print(f"✅ All {len(pending_users)} users APPROVED!")
    else:
        print("Users not approved")
else:
    print("\n✅ No pending users found!")

db.close()

print("\n" + "=" * 60)
print("DONE! Users can now login if approved.")
print("=" * 60)
