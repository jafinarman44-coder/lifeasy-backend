"""
Check existing tenant for email
"""
import sys
sys.path.append('E:/SUNNY/Jewel/APPERTMENT SOFTWER/LIFEASY_V27/backend')

from database_prod import SessionLocal
from models import Tenant

db = SessionLocal()

email = "majadar1din@gmail.com"

print("="*60)
print(f"🔍 CHECKING EMAIL: {email}")
print("="*60)

tenant = db.query(Tenant).filter(Tenant.email == email).first()

if tenant:
    print(f"\n✅ Tenant found!")
    print(f"   ID: {tenant.id}")
    print(f"   Name: {tenant.name}")
    print(f"   Email: {tenant.email}")
    print(f"   Phone: {tenant.phone}")
    print(f"   Verified: {'Yes' if tenant.is_verified else 'No'}")
    print(f"   Active: {'Yes' if tenant.is_active else 'No'}")
    print(f"   Created: {tenant.created_at}")
    
    if not tenant.is_verified:
        print("\n⚠️  Email NOT verified yet")
    elif not tenant.is_active:
        print("\n⚠️  Awaiting owner approval")
    else:
        print("\n✅ Account is active - You can login!")
else:
    print(f"\n❌ No tenant found with email: {email}")

db.close()
print("\n" + "="*60)
