"""
DEBUG 500 ERRORS - Test failing endpoints with detailed error capture
"""
import requests
import json

BASE_URL = "https://lifeasy-api.onrender.com"

print("\n" + "="*80)
print("🔍 DEBUGGING 500 ERRORS")
print("="*80 + "\n")

endpoints_to_test = [
    {
        "name": "Register",
        "method": "POST",
        "path": "/api/auth/register",
        "data": {
            "name": "Test User",
            "email": "testdebug@example.com",
            "phone": "+8801712345678",
            "password": "Test@1234"
        }
    },
    {
        "name": "Get Notifications (tenant_id=1)",
        "method": "GET",
        "path": "/api/notifications/1",
        "data": None
    },
    {
        "name": "Get Unread Notifications (tenant_id=1)",
        "method": "GET",
        "path": "/api/notifications/1/unread",
        "data": None
    },
    {
        "name": "Get Chat Rooms (tenant_id=1)",
        "method": "GET",
        "path": "/api/chat/rooms/1",
        "data": None
    },
    {
        "name": "Get Chat History (room_id=1)",
        "method": "GET",
        "path": "/api/chat/history/1",
        "data": None
    },
]

for endpoint in endpoints_to_test:
    print(f"\n{'='*80}")
    print(f"🧪 Testing: {endpoint['name']}")
    print(f"   {endpoint['method']} {endpoint['path']}")
    print(f"{'='*80}")
    
    try:
        url = f"{BASE_URL}{endpoint['path']}"
        headers = {"Content-Type": "application/json"}
        
        if endpoint['method'] == "GET":
            response = requests.get(url, headers=headers, timeout=15)
        else:
            response = requests.post(url, json=endpoint['data'], headers=headers, timeout=15)
        
        print(f"\n📊 Status Code: {response.status_code}")
        print(f"\n📝 Response Headers:")
        for key, value in response.headers.items():
            if key.lower() not in ['content-length', 'date', 'server']:
                print(f"   {key}: {value}")
        
        print(f"\n📄 Response Body:")
        try:
            # Try to parse as JSON and pretty print
            json_response = response.json()
            print(json.dumps(json_response, indent=2))
        except:
            # If not JSON, print raw text
            print(response.text[:1000])
        
        if response.status_code == 500:
            print(f"\n❌ INTERNAL SERVER ERROR DETECTED!")
            print(f"\n🔍 Likely causes:")
            print(f"   1. Database query error")
            print(f"   2. Missing/null field")
            print(f"   3. Wrong table/column name")
            print(f"   4. Import error")
        
    except requests.exceptions.Timeout:
        print("\n❌ REQUEST TIMEOUT (>15 seconds)")
    except Exception as e:
        print(f"\n❌ EXCEPTION: {str(e)}")

print("\n" + "="*80)
print("📋 NEXT STEPS:")
print("="*80)
print("""
1. Check Render logs at: https://dashboard.render.com
2. Look for Python traceback at the exact time you tested
3. The error will show:
   - File name and line number
   - Exception type (AttributeError, KeyError, etc.)
   - Full stack trace

Common fixes:
- Missing database table → Run migration
- Wrong column name → Check models.py
- Null value crash → Add null checks
- Import error → Check imports
""")
print("="*80 + "\n")
