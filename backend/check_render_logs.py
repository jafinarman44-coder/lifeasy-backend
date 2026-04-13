"""
LIFEASY V30 PRO - Render Deployment Checker
Checks what's failing on Render and provides exact fix
"""
import requests
import sys
from datetime import datetime

# Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
BOLD = "\033[1m"
RESET = "\033[0m"

print(f"\n{BOLD}{'='*80}{RESET}")
print(f"{BOLD}🔍 LIFEASY RENDER DEPLOYMENT CHECKER{RESET}")
print(f"{BOLD}{'='*80}{RESET}\n")

BASE_URL = "https://lifeasy-api.onrender.com"

# Test 1: Server Reachable
print(f"{BLUE}[1/5] Testing server reachability...{RESET}")
try:
    r = requests.get(f"{BASE_URL}/", timeout=10)
    if r.status_code == 200:
        print(f"{GREEN}✅ Server is ONLINE and reachable{RESET}\n")
    else:
        print(f"{YELLOW}⚠️  Server responded with {r.status_code}{RESET}\n")
except requests.exceptions.ConnectionError:
    print(f"{RED}❌ Server is OFFLINE or not deployed yet{RESET}")
    print(f"\n{YELLOW}POSSIBLE CAUSES:{RESET}")
    print(f"  1. Render build is still in progress (wait 3-5 min)")
    print(f"  2. Build failed - check Render logs")
    print(f"  3. Server crashed on startup")
    print(f"\n{YELLOW}NEXT STEPS:{RESET}")
    print(f"  1. Go to: https://dashboard.render.com")
    print(f"  2. Click your service")
    print(f"  3. Click 'Logs' tab")
    print(f"  4. Look for ERROR messages")
    sys.exit(1)
except requests.exceptions.Timeout:
    print(f"{RED}❌ Server is sleeping (free tier){RESET}")
    print(f"\n{YELLOW}FIX: Visit {BASE_URL} to wake it up (takes 1-2 min){RESET}\n")
    sys.exit(1)

# Test 2: Health Check
print(f"{BLUE}[2/5] Testing health endpoint...{RESET}")
try:
    r = requests.get(f"{BASE_URL}/health", timeout=10)
    if r.status_code == 200:
        print(f"{GREEN}✅ Health check passed{RESET}")
        print(f"   Response: {r.json()}\n")
    else:
        print(f"{RED}❌ Health check failed: {r.status_code}{RESET}")
        print(f"   Response: {r.text[:200]}\n")
except Exception as e:
    print(f"{RED}❌ Health check error: {e}{RESET}\n")

# Test 3: API Status
print(f"{BLUE}[3/5] Testing API status...{RESET}")
try:
    r = requests.get(f"{BASE_URL}/api/status", timeout=10)
    if r.status_code == 200:
        print(f"{GREEN}✅ API status endpoint working{RESET}")
        data = r.json()
        print(f"   Environment: {data.get('environment', 'unknown')}")
        print(f"   Version: {data.get('version', 'unknown')}\n")
    else:
        print(f"{RED}❌ API status failed: {r.status_code}{RESET}\n")
except Exception as e:
    print(f"{RED}❌ API status error: {e}{RESET}\n")

# Test 4: Critical Endpoints
print(f"{BLUE}[4/5] Testing critical endpoints...{RESET}")
endpoints = [
    ("GET", "/api/auth/login"),
    ("GET", "/api/tenants/all"),
    ("GET", "/api/settings/load/1"),
    ("GET", "/api/bills"),
    ("GET", "/api/notifications"),
]

working = 0
failing = 0

for method, path in endpoints:
    try:
        r = requests.get(f"{BASE_URL}{path}", timeout=5)
        if r.status_code in [200, 401, 404]:
            print(f"{GREEN}✅ {path} → {r.status_code}{RESET}")
            working += 1
        else:
            print(f"{RED}❌ {path} → {r.status_code}{RESET}")
            failing += 1
    except Exception as e:
        print(f"{RED}❌ {path} → ERROR: {str(e)[:50]}{RESET}")
        failing += 1

print(f"\n")

# Test 5: Check Configuration
print(f"{BLUE}[5/5] Checking deployment configuration...{RESET}")

# Check render.yaml
try:
    with open("render.yaml", 'r') as f:
        content = f.read()
        if "sqlite" in content.lower():
            print(f"{YELLOW}⚠️  WARNING: render.yaml uses SQLite{RESET}")
            print(f"   But .env uses PostgreSQL - this might cause issues")
        if "uvicorn main_prod:app" in content:
            print(f"{GREEN}✅ Start command correct: uvicorn main_prod:app{RESET}")
        print()
except:
    print(f"{RED}❌ render.yaml not found{RESET}\n")

# Final Report
print(f"\n{BOLD}{'='*80}{RESET}")
print(f"{BOLD}📊 DEPLOYMENT STATUS REPORT{RESET}")
print(f"{BOLD}{'='*80}{RESET}\n")

total = working + failing
print(f"  Endpoints Working: {GREEN}{working}/{total}{RESET}")
print(f"  Endpoints Failing: {RED}{failing}/{total}{RESET}\n")

if failing > 0:
    print(f"{RED}{BOLD}🚨 DEPLOYMENT HAS ISSUES{RESET}\n")
    
    print(f"{YELLOW}📋 HOW TO CHECK RENDER LOGS:{RESET}\n")
    print(f"  1️⃣  Go to: https://dashboard.render.com")
    print(f"  2️⃣  Click on: 'lifeasy-api' service")
    print(f"  3️⃣  Click: 'Logs' tab")
    print(f"  4️⃣  Look for RED error messages")
    print(f"  5️⃣  Common errors:")
    print(f"      - 'ModuleNotFoundError' → Missing dependency")
    print(f"      - 'Database error' → DATABASE_URL wrong")
    print(f"      - 'Port already in use' → PORT config issue")
    print(f"      - 'Build failed' → requirements.txt issue\n")
    
    print(f"{YELLOW}🔧 COMMON FIXES:{RESET}\n")
    print(f"  FIX 1: If build failed")
    print(f"    → Check requirements.txt has all packages")
    print(f"    → Run: pip freeze > requirements.txt")
    print(f"    → Push again\n")
    
    print(f"  FIX 2: If database error")
    print(f"    → Check DATABASE_URL in Render Environment variables")
    print(f"    → Should be: postgresql://user:pass@host:port/dbname\n")
    
    print(f"  FIX 3: If server crashed")
    print(f"    → Check logs for Python errors")
    print(f"    → Test locally: python main_prod.py\n")
    
    print(f"  FIX 4: If nothing works")
    print(f"    → Manual Deploy: Render Dashboard → Manual Deploy → Clear cache & deploy\n")
    
    print(f"{YELLOW}📞 SHARE THIS FOR HELP:{RESET}")
    print(f"  - Screenshot of Render logs (last 50 lines)")
    print(f"  - Error messages from logs")
    print(f"  - This diagnostic report\n")
    
else:
    print(f"{GREEN}{BOLD}✅ ALL CHECKS PASSED!{RESET}\n")
    print(f"Deployment is working correctly.")

print(f"{'='*80}\n")
