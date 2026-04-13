"""
Complete OTP Registration Flow Test
"""
import requests
import time

BASE_URL = "http://192.168.0.181:8000/api"

print("="*70)
print("🧪 COMPLETE OTP REGISTRATION FLOW TEST")
print("="*70)

# Test data
test_email = "majadar1din@gmail.com"
test_password = "123456"
test_name = "Test User"
test_phone = "+8801700000000"

# Step 1: Request OTP
print(f"\n📤 STEP 1: Requesting OTP...")
print(f"   Email: {test_email}")
print(f"   Name: {test_name}")

response1 = requests.post(
    f"{BASE_URL}/auth/v2/register-request",
    json={
        "email": test_email,
        "password": test_password,
        "name": test_name,
        "phone": test_phone
    }
)

result1 = response1.json()
print(f"   Status: {response1.status_code}")
print(f"   Response: {result1}")

if result1.get("status") != "success":
    print("   ❌ FAILED at Step 1!")
    exit(1)

print("   ✅ OTP sent successfully!")
print("\n⏳ Waiting 2 seconds for email delivery...")
time.sleep(2)

# Step 2: Ask user for OTP
print("\n" + "="*70)
otp_received = input("🔢 Enter the OTP you received (or '999888' to test): ").strip()

if not otp_received:
    print("❌ No OTP entered!")
    exit(1)

# Step 3: Verify OTP
print(f"\n✅ Verifying OTP: {otp_received[:3]}***")
response2 = requests.post(
    f"{BASE_URL}/auth/v2/register-verify",
    json={
        "email": test_email,
        "otp": otp_received
    }
)

result2 = response2.json()
print(f"   Status: {response2.status_code}")
print(f"   Response: {result2}")

if result2.get("status") == "success":
    print("\n🎉 SUCCESS! OTP verified!")
    print(f"   Tenant ID: {result2.get('tenant_id')}")
    print(f"   Approval Status: {result2.get('approval_status')}")
    print(f"   Message: {result2.get('message')}")
else:
    print(f"\n❌ Verification failed!")
    print(f"   Error: {result2.get('message', 'Unknown error')}")

print("\n" + "="*70)
