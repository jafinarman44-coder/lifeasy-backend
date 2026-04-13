"""
LIFEASY V30 PRO - Render Startup Error Simulator
Tests what causes "Exited with status 1" on Render
"""
import os
import sys
from dotenv import load_dotenv

# Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
BOLD = "\033[1m"
RESET = "\033[0m"

print(f"\n{BOLD}{'='*80}{RESET}")
print(f"{BOLD}🔍 RENDER 'Exited with status 1' DIAGNOSTIC{RESET}")
print(f"{BOLD}{'='*80}{RESET}\n")

# Load .env
load_dotenv()

errors_found = []

# Test 1: Check main_prod.py can be imported
print(f"{BLUE}[1/7] Testing main_prod.py import...{RESET}")
try:
    sys.path.insert(0, '.')
    from main_prod import app
    print(f"{GREEN}✅ main_prod.py imports successfully{RESET}\n")
except Exception as e:
    print(f"{RED}❌ main_prod.py import FAILED{RESET}")
    print(f"   Error: {str(e)}\n")
    errors_found.append(f"Import error: {e}")

# Test 2: Check database connection
print(f"{BLUE}[2/7] Testing database connection...{RESET}")
DATABASE_URL = os.getenv("DATABASE_URL")
print(f"   DATABASE_URL: {DATABASE_URL[:50] if DATABASE_URL else 'NOT SET'}...")

if not DATABASE_URL:
    print(f"{RED}❌ DATABASE_URL not set!{RESET}\n")
    errors_found.append("DATABASE_URL missing")
else:
    try:
        from sqlalchemy import create_engine, text
        engine = create_engine(DATABASE_URL)
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        print(f"{GREEN}✅ Database connection successful{RESET}\n")
    except Exception as e:
        print(f"{RED}❌ Database connection FAILED{RESET}")
        print(f"   Error: {str(e)}\n")
        errors_found.append(f"Database error: {e}")

# Test 3: Check all router imports
print(f"{BLUE}[3/7] Testing router imports...{RESET}")
routers_to_test = [
    "routers.auth_phase6",
    "routers.auth_v2",
    "routers.notification_router",
    "routers.chat_router",
    "routers.chat_router_v2",
    "routers.chat_v3",
    "routers.chat_block_router",
    "routers.chat_call_router",
    "routers.call_router",
    "routers.call_router_v2",
    "routers.bill_router",
    "routers.tenant_router",
    "routers.settings_router",
    "routers.group_router",
    "routers.media_router",
    "auth_master",
    "payment_gateway",
    "notification_service",
]

imported = 0
failed = 0

for router in routers_to_test:
    try:
        __import__(router)
        imported += 1
    except Exception as e:
        print(f"{RED}❌ {router}: {str(e)[:60]}{RESET}")
        failed += 1
        errors_found.append(f"Router {router}: {e}")

if failed == 0:
    print(f"{GREEN}✅ All {imported} routers imported successfully{RESET}\n")
else:
    print(f"\n{RED}❌ {failed} routers failed to import{RESET}\n")

# Test 4: Check required packages
print(f"{BLUE}[4/7] Checking required packages...{RESET}")
required_packages = [
    "fastapi",
    "uvicorn",
    "sqlalchemy",
    "psycopg2",
    "python-jose",
    "passlib",
    "pydantic",
    "dotenv",
]

missing = []
for package in required_packages:
    try:
        __import__(package.replace("-", "_"))
    except ImportError:
        missing.append(package)
        print(f"{RED}❌ Missing: {package}{RESET}")

if not missing:
    print(f"{GREEN}✅ All required packages installed{RESET}\n")
else:
    print(f"\n{RED}❌ {len(missing)} packages missing{RESET}\n")
    errors_found.append(f"Missing packages: {', '.join(missing)}")

# Test 5: Check environment variables
print(f"{BLUE}[5/7] Checking environment variables...{RESET}")
required_vars = [
    "DATABASE_URL",
    "LIFEASY_ENV",
    "SECRET_KEY_V2",
]

missing_vars = []
for var in required_vars:
    value = os.getenv(var)
    if not value:
        print(f"{RED}❌ {var}: NOT SET{RESET}")
        missing_vars.append(var)
    else:
        print(f"{GREEN}✅ {var}: SET{RESET}")

if missing_vars:
    print(f"\n{RED}❌ {len(missing_vars)} environment variables missing{RESET}\n")
    errors_found.append(f"Missing env vars: {', '.join(missing_vars)}")
else:
    print()

# Test 6: Check port configuration
print(f"{BLUE}[6/7] Checking port configuration...{RESET}")
PORT = os.getenv("PORT", "8000")
print(f"   PORT: {PORT}")
print(f"{GREEN}✅ Port configuration OK{RESET}\n")

# Test 7: Simulate app startup
print(f"{BLUE}[7/7] Simulating app startup...{RESET}")
try:
    from main_prod import app
    print(f"{GREEN}✅ App created successfully{RESET}")
    print(f"   Title: {app.title}")
    print(f"   Version: {app.version}\n")
except Exception as e:
    print(f"{RED}❌ App creation FAILED{RESET}")
    print(f"   Error: {str(e)}\n")
    errors_found.append(f"App creation: {e}")

# Final Report
print(f"\n{BOLD}{'='*80}{RESET}")
print(f"{BOLD}📊 DIAGNOSTIC REPORT{RESET}")
print(f"{BOLD}{'='*80}{RESET}\n")

if errors_found:
    print(f"{RED}{BOLD}❌ FOUND {len(errors_found)} ERROR(S):{RESET}\n")
    for i, error in enumerate(errors_found, 1):
        print(f"{RED}[{i}] {error}{RESET}")
    
    print(f"\n{YELLOW}🔧 LIKELY CAUSE OF 'Exited with status 1':{RESET}\n")
    
    if any("Database" in e for e in errors_found):
        print(f"  💥 DATABASE CONNECTION FAILED")
        print(f"     → Check DATABASE_URL in Render Environment Variables")
        print(f"     → Must be: postgresql://user:pass@host:port/dbname")
        print(f"     → Current: {DATABASE_URL[:30] if DATABASE_URL else 'NOT SET'}...\n")
    
    if any("import" in e.lower() for e in errors_found):
        print(f"  💥 IMPORT ERROR")
        print(f"     → Missing dependency in requirements.txt")
        print(f"     → Run: pip freeze > requirements.txt")
        print(f"     → Push to Render\n")
    
    if any("missing" in e.lower() for e in errors_found):
        print(f"  💥 MISSING CONFIGURATION")
        print(f"     → Set required environment variables in Render")
        print(f"     → Check .env.example for required vars\n")
    
    print(f"{YELLOW}📋 EXACT FIXES:{RESET}\n")
    print(f"  1. Check Render logs for exact error line")
    print(f"  2. Fix the error shown above")
    print(f"  3. Push to Git")
    print(f"  4. Render will auto-deploy\n")
    
    sys.exit(1)
else:
    print(f"{GREEN}{BOLD}✅ ALL CHECKS PASSED!{RESET}\n")
    print(f"App should start successfully on Render.")
    print(f"If still failing, check Render logs for runtime errors.\n")
    sys.exit(0)
