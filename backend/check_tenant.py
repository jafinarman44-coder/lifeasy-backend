"""
Check if specific tenant exists in database
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
EMAIL_TO_CHECK = "majadar1din@gmail.com"

engine = create_engine(DATABASE_URL)

print(f"🔍 Checking tenant: {EMAIL_TO_CHECK}\n")

with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT id, tenant_id, name, email, phone, building, flat, 
               is_verified, is_active, created_at
        FROM tenants 
        WHERE email = :email
    """), {"email": EMAIL_TO_CHECK})
    
    tenant = result.fetchone()
    
    if tenant:
        print("✅ Tenant found!")
        print(f"\n📋 Tenant Details:")
        print(f"   ID: {tenant[0]}")
        print(f"   Tenant ID: {tenant[1]}")
        print(f"   Name: {tenant[2]}")
        print(f"   Email: {tenant[3]}")
        print(f"   Phone: {tenant[4] or 'Not set'}")
        print(f"   Building: {tenant[5] or 'Not set'}")
        print(f"   Flat: {tenant[6] or 'Not set'}")
        print(f"   Is Verified: {tenant[7]}")
        print(f"   Is Active: {tenant[8]}")
        print(f"   Created At: {tenant[9]}")
        
        if not tenant[7]:
            print("\n⚠️  WARNING: is_verified is FALSE")
            print("   Fix: UPDATE tenants SET is_verified = TRUE WHERE email = :email;")
        
        if not tenant[8]:
            print("\n⚠️  WARNING: is_active is FALSE")
            print("   Fix: UPDATE tenants SET is_active = TRUE WHERE email = :email;")
            
    else:
        print(f"❌ Tenant NOT found with email: {EMAIL_TO_CHECK}")
        print("\n📝 This email is not registered in the database.")
        print("   User needs to complete registration first.")
    
    conn.close()
