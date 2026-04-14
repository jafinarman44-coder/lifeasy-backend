"""
CRITICAL API ERROR DETECTOR
Tests all endpoints and captures exact 500 errors with details
"""
import requests
import json
import sys
from datetime import datetime

BASE_URL = "https://lifeasy-api.onrender.com"

# Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
BOLD = "\033[1m"
RESET = "\033[0m"

print(f"\n{BOLD}{'='*80}{RESET}")
print(f"{BOLD}🚨 CRITICAL API ERROR DETECTOR{RESET}")
print(f"{BOLD}{'='*80}{RESET}\n")
print(f"📍 Target: {BASE_URL}")
print(f"📍 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Track errors
critical_errors = []
all_results = []

def test_api(method, path, name, data=None, auth_token=None):
    """Test API and capture detailed errors"""
    url = f"{BASE_URL}{path}"
    headers = {"Content-Type": "application/json"}
    
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"
    
    print(f"{BLUE}📥 Testing: {name}{RESET}")
    print(f"   {method} {path}")
    
    try:
        start = datetime.now()
        
        if method == "GET":
            resp = requests.get(url, headers=headers, timeout=15)
        elif method == "POST":
            resp = requests.post(url, json=data, headers=headers, timeout=15)
        
        duration = (datetime.now() - start).total_seconds()
        
        # Color based on status
        if resp.status_code == 200:
            status_color = GREEN
            status_icon = "✅"
        elif resp.status_code == 401 or resp.status_code == 404:
            status_color = YELLOW
            status_icon = "⚠️"
        else:
            status_color = RED
            status_icon = "❌"
        
        print(f"{status_icon} Status: {status_color}{resp.status_code}{RESET} | Time: {duration:.2f}s")
        
        # Try to get response body
        try:
            body = resp.json()
            if resp.status_code >= 500:
                print(f"{RED}   ERROR RESPONSE: {json.dumps(body, indent=4)}{RESET}")
                critical_errors.append({
                    "name": name,
                    "method": method,
                    "path": path,
                    "status": resp.status_code,
                    "response": body,
                    "duration": duration
                })
        except:
            if resp.status_code >= 500:
                print(f"{RED}   ERROR RESPONSE: {resp.text[:500]}{RESET}")
                critical_errors.append({
                    "name": name,
                    "method": method,
                    "path": path,
                    "status": resp.status_code,
                    "response": resp.text[:500],
                    "duration": duration
                })
        
        all_results.append({
            "name": name,
            "path": path,
            "status": resp.status_code,
            "duration": duration
        })
        
        return resp
        
    except requests.exceptions.Timeout:
        print(f"{RED}❌ TIMEOUT - Request took more than 15s{RESET}")
        critical_errors.append({
            "name": name,
            "method": method,
            "path": path,
            "status": "TIMEOUT",
            "response": "Request timed out",
            "duration": 15
        })
    except Exception as e:
        print(f"{RED}❌ EXCEPTION: {str(e)}{RESET}")
        critical_errors.append({
            "name": name,
            "method": method,
            "path": path,
            "status": "EXCEPTION",
            "response": str(e),
            "duration": 0
        })

# ============================================
# TEST ALL CRITICAL ENDPOINTS
# ============================================

print(f"{BOLD}{'='*80}{RESET}\n")

# 1. Health & Status (Should be 200)
print(f"{BOLD}[1] Basic Endpoints{RESET}")
print(f"{'-'*80}")
test_api("GET", "/", "Root Endpoint")
test_api("GET", "/health", "Health Check")
test_api("GET", "/api/status", "API Status")
print()

# 2. Auth Endpoints (Critical - Often fail)
print(f"{BOLD}[2] Authentication Endpoints{RESET}")
print(f"{'-'*80}")
test_api("POST", "/api/auth/login", "Login V1", {
    "email": "majadar1din@gmail.com",
    "password": "Jewel@1234"
})
test_api("POST", "/api/auth/v2/login", "Login V2", {
    "email": "majadar1din@gmail.com",
    "password": "Jewel@1234"
})
test_api("POST", "/api/auth/register", "Register", {
    "full_name": "Test User",
    "email": "test@example.com",
    "password": "Test@123",
    "phone": "+8801712345678"
})
print()

# 3. User/Tenant Endpoints
print(f"{BOLD}[3] Tenant/User Endpoints{RESET}")
print(f"{'-'*80}")
test_api("GET", "/api/tenants/all", "List Tenants")
test_api("GET", "/api/tenants/profile/1", "Tenant Profile (ID=1)")
print()

# 4. Notification Endpoints
print(f"{BOLD}[4] Notification Endpoints{RESET}")
print(f"{'-'*80}")
test_api("GET", "/api/notifications/1", "Get Notifications (tenant_id=1)")
test_api("GET", "/api/notifications/1/unread", "Unread Count (tenant_id=1)")
print()

# 5. Chat Endpoints
print(f"{BOLD}[5] Chat Endpoints{RESET}")
print(f"{'-'*80}")
test_api("GET", "/api/chat/rooms/1", "Chat Rooms (tenant_id=1)")
test_api("GET", "/api/chat/history/1", "Chat History (room_id=1)")
print()

# 6. Bill Endpoints
print(f"{BOLD}[6] Bill Endpoints{RESET}")
print(f"{'-'*80}")
test_api("GET", "/api/bills/tenant/1", "List Bills (tenant_id=1)")
print()

# 7. Settings Endpoints
print(f"{BOLD}[7] Settings Endpoints{RESET}")
print(f"{'-'*80}")
test_api("GET", "/api/settings/load/1", "Get Settings (tenant_id=1)")
print()

# ============================================
# FINAL REPORT
# ============================================
print(f"\n{BOLD}{'='*80}{RESET}")
print(f"{BOLD}📊 ERROR REPORT{RESET}")
print(f"{BOLD}{'='*80}{RESET}\n")

total = len(all_results)
passed = len([r for r in all_results if r["status"] == 200])
warnings = len([r for r in all_results if r["status"] in [401, 404]])
errors = len(critical_errors)

print(f"{BOLD}Summary:{RESET}")
print(f"  Total APIs Tested: {total}")
print(f"  {GREEN}✅ Passed (200): {passed}{RESET}")
print(f"  {YELLOW}⚠️  Warnings (401/404): {warnings}{RESET}")
print(f"  {RED}❌ Critical Errors (500+): {errors}{RESET}")
print()

if critical_errors:
    print(f"{BOLD}{RED}🚨 CRITICAL ERRORS FOUND:{RESET}\n")
    
    for i, error in enumerate(critical_errors, 1):
        print(f"{RED}{BOLD}[Error #{i}]{RESET}")
        print(f"  API: {error['name']}")
        print(f"  Route: {error['method']} {error['path']}")
        print(f"  Status: {error['status']}")
        print(f"  Response: {json.dumps(error['response'], indent=4) if isinstance(error['response'], dict) else error['response']}")
        print(f"  Duration: {error['duration']:.2f}s")
        print()
    
    print(f"{YELLOW}📋 NEXT STEPS:{RESET}")
    print(f"  1. Check Render logs at: https://dashboard.render.com")
    print(f"  2. Look for errors at the exact time you tested")
    print(f"  3. The failing routes are listed above")
    print(f"  4. Fix the Python code for those routes")
else:
    print(f"{GREEN}{BOLD}✅ NO 500 ERRORS FOUND!{RESET}")
    print(f"\nAll endpoints are working properly.")
    print(f"If app is still failing, check:")
    print(f"  - CORS configuration")
    print(f"  - Request headers from app")
    print(f"  - Network connectivity")

print(f"\n{BOLD}{'='*80}{RESET}\n")

# Exit with error code if critical errors found
if critical_errors:
    sys.exit(1)
else:
    sys.exit(0)
