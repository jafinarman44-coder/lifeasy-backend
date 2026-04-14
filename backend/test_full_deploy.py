import requests
import json

print("\n" + "="*80)
print("COMPREHENSIVE RENDER DEPLOYMENT TEST")
print("="*80 + "\n")

BASE_URL = "https://lifeasy-api.onrender.com"

# Test all critical endpoints
endpoints = [
    ("GET", "/", "Root"),
    ("GET", "/health", "Health Check"),
    ("GET", "/api/status", "API Status"),
    ("POST", "/api/auth/login", "Login V1"),
    ("POST", "/api/auth/v2/login", "Login V2"),
    ("POST", "/api/auth/register", "Register"),
    ("GET", "/api/tenants/all", "List Tenants"),
    ("GET", "/api/tenants", "List Tenants (alt)"),
    ("GET", "/api/tenants/profile", "Tenant Profile"),
    ("GET", "/api/notifications", "Notifications"),
    ("GET", "/api/notifications/count", "Notification Count"),
    ("GET", "/api/chat/v2/conversations", "Chat Conversations"),
    ("GET", "/api/chat/v3/health", "Chat V3 Health"),
    ("GET", "/api/bills", "List Bills"),
    ("GET", "/api/settings/load/1", "Settings Load"),
    ("GET", "/api/settings", "Settings"),
]

results = []

for method, path, name in endpoints:
    try:
        if method == "GET":
            response = requests.get(f"{BASE_URL}{path}", timeout=10)
        else:
            response = requests.post(f"{BASE_URL}{path}", json={}, timeout=10)
        
        status = response.status_code
        # Consider 401 as "working" (needs auth but endpoint exists)
        if status in [200, 401, 400]:
            verdict = "✅ WORKING"
        elif status == 404:
            verdict = "❌ 404 - NOT FOUND"
        else:
            verdict = f"⚠️  {status}"
        
        results.append((name, path, status, verdict))
        print(f"{verdict:20} | {status:3} | {name:25} | {path}")
        
    except Exception as e:
        results.append((name, path, "ERROR", str(e)))
        print(f"❌ ERROR             |     | {name:25} | {path}")

# Summary
print("\n" + "="*80)
print("SUMMARY REPORT")
print("="*80 + "\n")

total = len(results)
working = sum(1 for r in results if "WORKING" in r[3])
not_found = sum(1 for r in results if "404" in r[3])
errors = sum(1 for r in results if "ERROR" in r[3])

print(f"Total Endpoints:  {total}")
print(f"✅ Working:       {working}")
print(f"❌ 404 Errors:    {not_found}")
print(f"⚠️  Other Errors: {errors}")
print(f"\nSuccess Rate:     {(working/total*100):.1f}%\n")

if working >= 12:
    print("✅ EXCELLENT - Most APIs are working!")
elif working >= 8:
    print("⚠️  GOOD - Most APIs working, some issues")
elif working >= 4:
    print("❌ FAIR - Several APIs not working")
else:
    print("❌ POOR - Major deployment issue")

print("\n" + "="*80)

# Show 404 endpoints
if not_found > 0:
    print("\n❌ ENDPOINTS RETURNING 404:\n")
    for name, path, status, verdict in results:
        if "404" in verdict:
            print(f"  {path} ({name})")
    
    print("\n⚠️  These routes are NOT registered on Render!")
    print("   This means main_prod.py on Render is still old code.")

print("\n" + "="*80 + "\n")
