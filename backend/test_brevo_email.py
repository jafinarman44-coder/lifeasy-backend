# LIFEASY - Brevo Email Test Script
# Test OTP email sending with Brevo API

import requests
import json

print("🧪 Testing Brevo OTP Email Service")
print("=" * 50)

# Your test email
TEST_EMAIL = "yourtestemail@gmail.com"  # Change this to your real email

# API endpoint
url = "http://localhost:8000/api/auth/v2/register-request"

# Test payload
payload = {
    "email": TEST_EMAIL,
    "password": "123456",
    "phone": "01700000000",
    "name": "Test User"
}

print(f"\n📤 Sending POST request to: {url}")
print(f"📧 Test email: {TEST_EMAIL}")
print("\nPayload:")
print(json.dumps(payload, indent=2))

try:
    response = requests.post(url, json=payload)
    
    print(f"\n📊 Response Status: {response.status_code}")
    print(f"📄 Response Body:")
    print(json.dumps(response.json(), indent=2))
    
    if response.status_code == 200:
        print("\n✅ SUCCESS! OTP email sent via Brevo!")
        print("📬 Check your inbox at:", TEST_EMAIL)
    else:
        print("\n❌ Request failed. Check the error above.")
        
except requests.exceptions.ConnectionError:
    print("\n❌ CONNECTION ERROR!")
    print("Make sure the backend is running:")
    print("   cd LIFEASY_V27/backend")
    print("   uvicorn main_prod:app --reload")
except Exception as e:
    print(f"\n❌ Error: {e}")

print("\n" + "=" * 50)
print("Test completed!")
