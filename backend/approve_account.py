"""
Approve tenant account for login
"""
import sys
sys.path.append('E:/SUNNY/Jewel/APPERTMENT SOFTWER/LIFEASY_V27/backend')

from database_prod import SessionLocal
from models import Tenant

db = SessionLocal()

email = "majadar1din@gmail.com"

print("="*60)
print("🔑 APPROVING TENANT ACCOUNT")
print("="*60)

tenant = db.query(Tenant).filter(Tenant.email == email).first()

if not tenant:
    print("❌ Tenant not found!")
    db.close()
    exit(1)

print(f"\nCurrent Status:")
print(f"   Name: {tenant.name}")
print(f"   Email: {tenant.email}")
print(f"   Verified: {'Yes' if tenant.is_verified else 'No'}")
print(f"   Active: {'Yes' if tenant.is_active else 'No'}")

# Approve the account
tenant.is_active = True
db.commit()

print(f"\n✅ Account approved successfully!")
print(f"   You can now login with:")
print(f"   Email: {tenant.email}")
print(f"   Password: Your registered password")

db.close()
print("\n" + "="*60)
