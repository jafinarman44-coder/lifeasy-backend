"""
Test my-profile endpoint - Just viewing, no changes
"""
import requests
import json

tenant_id = 2  # jafinarman44@gmail.com

url = f"http://192.168.0.181:8000/api/auth/v2/my-profile?tenant_id={tenant_id}"

print("="*60)
print(f"📡 Testing: GET /auth/v2/my-profile")
print(f"   Tenant ID: {tenant_id}")
print("="*60)

try:
    response = requests.get(url)
    
    print(f"\n📊 Status Code: {response.status_code}")
    print(f"\n📄 Full JSON Response:")
    print("-"*60)
    print(json.dumps(response.json(), indent=2))
    print("-"*60)
except Exception as e:
    print(f"\n❌ Error: {e}")

print("\n" + "="*60)
