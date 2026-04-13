"""
Full OTP Flow Test - Backend + Email
"""
import requests
import random

BASE_URL = "http://192.168.0.181:8000/api"

print("="*70)
print("🧪 FULL OTP REGISTRATION TEST")
print("="*70)

# Step 1: Register Request (Send OTP)
test_email = "majadar1din@gmail.com"
test_password = "123456"
test_name = "Test User"
test_phone = "+8801700000000"

print(f"\n📤 STEP 1: Sending registration request...")
print(f"   Email: {test_email}")
print(f"   Name: {test_name}")

response = requests.post(
    f"{BASE_URL}/auth/v2/register-request",
    json={
        "email": test_email,
        "password": test_password,
        "name": test_name,
        "phone": test_phone
    }
)

result = response.json()
print(f"   Status Code: {response.status_code}")
print(f"   Response: {result}")

if result.get("status") == "success":
    print("   ✅ OTP sent successfully!")
    print(f"\n📧 CHECK YOUR EMAIL: {test_email}")
    print("   • Check Inbox folder")
    print("   • Check SPAM/JUNK folder")
    print("   • Check Promotions tab (Gmail)")
    print("\n⏳ Waiting for you to receive the OTP...")
    
    # Ask user to enter OTP they received
    otp_received = input("\n🔢 Enter the OTP you received: ").strip()
    
    if otp_received:
        print(f"\n✅ Verifying OTP: {otp_received}")
        
        # Step 2: Verify OTP
        verify_response = requests.post(
            f"{BASE_URL}/auth/v2/register-verify",
            json={
                "email": test_email,
                "otp": otp_received
            }
        )
        
        verify_result = verify_response.json()
        print(f"   Status Code: {verify_response.status_code}")
        print(f"   Response: {verify_result}")
        
        if verify_result.get("status") == "success":
            print("   ✅ OTP verified successfully!")
            print(f"\n🎉 REGISTRATION COMPLETE!")
            print(f"   Tenant ID: {verify_result.get('tenant_id')}")
            print(f"   Approval Status: {verify_result.get('approval_status')}")
        else:
            print(f"   ❌ Verification failed: {verify_result.get('message', 'Unknown error')}")
    else:
        print("   ⚠️ No OTP entered. You can manually verify later.")
else:
    print(f"   ❌ Failed to send OTP: {result.get('message', 'Unknown error')}")

print("\n" + "="*70)
