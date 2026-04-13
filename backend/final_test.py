"""
Final Test - Complete Registration Flow
"""
import requests
import time

BASE_URL = "http://192.168.0.181:8000/api"

print("="*70)
print("🧪 FINAL REGISTRATION TEST")
print("="*70)

test_email = "majadar1din@gmail.com"
test_password = "123456"
test_name = "Jewel"
test_phone = "+8801700000000"

# Step 1: Request OTP
print(f"\n📤 STEP 1: Sending registration request...")
response1 = requests.post(
    f"{BASE_URL}/auth/v2/register-request",
    json={
        "email": test_email,
        "password": test_password,
        "name": test_name,
        "phone": test_phone
    }
)

print(f"   Status: {response1.status_code}")
try:
    result1 = response1.json()
    print(f"   Response: {result1}")
except:
    print(f"   Raw: {response1.text}")
    exit(1)

if result1.get("status") != "success":
    print("   ❌ FAILED!")
    exit(1)

print("   ✅ OTP sent!")

# Step 2: Verify OTP (use latest from database)
print(f"\n🔍 Checking database for latest OTP...")
import sys
sys.path.append('E:/SUNNY/Jewel/APPERTMENT SOFTWER/LIFEASY_V27/backend')
from database_prod import SessionLocal
from models import OTPCode

db = SessionLocal()
latest_otp = db.query(OTPCode).filter(
    OTPCode.email == test_email,
    OTPCode.is_used == False
).order_by(OTPCode.created_at.desc()).first()

if not latest_otp:
    print("   ❌ No OTP found!")
    exit(1)

otp_code = latest_otp.otp
print(f"   Found OTP: {otp_code}")
db.close()

time.sleep(1)

# Step 3: Verify
print(f"\n✅ STEP 2: Verifying OTP {otp_code}...")
response2 = requests.post(
    f"{BASE_URL}/auth/v2/register-verify",
    json={
        "email": test_email,
        "otp": otp_code
    }
)

print(f"   Status: {response2.status_code}")
try:
    result2 = response2.json()
    print(f"   Response: {result2}")
    
    if result2.get("status") == "success":
        print("\n🎉 SUCCESS! Registration complete!")
        print(f"   Tenant ID: {result2.get('tenant_id')}")
        print(f"   Approval: {result2.get('approval_status')}")
    else:
        print(f"\n❌ Verification failed: {result2.get('message')}")
except Exception as e:
    print(f"   Error: {e}")
    print(f"   Raw: {response2.text}")

print("\n" + "="*70)
