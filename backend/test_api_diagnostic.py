"""
LIFEASY V30 PRO - API Diagnostic Test Script
Tests all critical endpoints and identifies failures

Usage:
python test_api_diagnostic.py
"""
import requests
import json
import sys
from datetime import datetime

# ============================================
# CONFIGURATION
# ============================================
BASE_URL = "https://lifeasy-api.onrender.com"
# For local testing: BASE_URL = "http://localhost:8000"

# Color codes for terminal output
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

# Test results tracking
results = {
    "passed": [],
    "failed": [],
    "skipped": []
}

def log_test(name, status_code, response_time, details=""):
    """Log test results with colors"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    if status_code == 200:
        results["passed"].append(name)
        print(f"{GREEN}✅ [{timestamp}] {name}{RESET}")
        print(f"   Status: {status_code} | Time: {response_time:.2f}s")
    elif status_code == 0:
        results["failed"].append(name)
        print(f"{RED}❌ [{timestamp}] {name}{RESET}")
        print(f"   ERROR: Connection failed - Server unreachable")
    else:
        results["failed"].append(name)
        print(f"{RED}❌ [{timestamp}] {name}{RESET}")
        print(f"   Status: {status_code} | Time: {response_time:.2f}s")
    
    if details:
        print(f"   Details: {details}")
    print()

def test_endpoint(method, path, name, data=None, headers=None, expected_status=200):
    """Test a single endpoint"""
    url = f"{BASE_URL}{path}"
    
    try:
        start_time = datetime.now()
        
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=10)
        elif method == "PUT":
            response = requests.put(url, json=data, headers=headers, timeout=10)
        elif method == "DELETE":
            response = requests.delete(url, headers=headers, timeout=10)
        
        response_time = (datetime.now() - start_time).total_seconds()
        
        # Try to parse response JSON
        try:
            response_data = response.json()
        except:
            response_data = response.text[:200]
        
        log_test(name, response.status_code, response_time, str(response_data))
        
        return response
        
    except requests.exceptions.ConnectionError:
        log_test(name, 0, 0, "Cannot connect to server. Check if it's running.")
        return None
    except requests.exceptions.Timeout:
        log_test(name, 0, 10, "Request timed out. Server might be slow or down.")
        return None
    except Exception as e:
        log_test(name, 0, 0, f"Exception: {str(e)}")
        return None

# ============================================
# TEST SUITE
# ============================================

def test_basic_connectivity():
    """Test 1: Basic server connectivity"""
    print(f"\n{BLUE}{'='*80}{RESET}")
    print(f"{BLUE}TEST 1: Basic Connectivity{RESET}")
    print(f"{BLUE}{'='*80}{RESET}\n")
    
    test_endpoint("GET", "/", "Root Endpoint")
    test_endpoint("GET", "/health", "Health Check")
    test_endpoint("GET", "/api/status", "API Status")
    test_endpoint("GET", "/docs", "API Documentation")

def test_auth_endpoints():
    """Test 2: Authentication endpoints"""
    print(f"\n{BLUE}{'='*80}{RESET}")
    print(f"{BLUE}TEST 2: Authentication Endpoints{RESET}")
    print(f"{BLUE}{'='*80}{RESET}\n")
    
    # Test registration
    test_endpoint(
        "POST", "/api/auth/register",
        "Register User",
        data={
            "full_name": "Test User",
            "email": "test@example.com",
            "password": "Test@123",
            "phone": "+8801712345678"
        }
    )
    
    # Test login
    test_endpoint(
        "POST", "/api/auth/login",
        "Login User",
        data={
            "email": "test@example.com",
            "password": "Test@123"
        }
    )
    
    # Test V2 login
    test_endpoint(
        "POST", "/api/auth/v2/login",
        "V2 Login",
        data={
            "email": "test@example.com",
            "password": "Test@123"
        }
    )

def test_user_endpoints():
    """Test 3: User/Tenant endpoints"""
    print(f"\n{BLUE}{'='*80}{RESET}")
    print(f"{BLUE}TEST 3: User/Tenant Endpoints{RESET}")
    print(f"{BLUE}{'='*80}{RESET}\n")
    
    test_endpoint("GET", "/api/tenants", "List Tenants")
    test_endpoint("GET", "/api/tenants/profile", "Tenant Profile")

def test_notification_endpoints():
    """Test 4: Notification endpoints"""
    print(f"\n{BLUE}{'='*80}{RESET}")
    print(f"{BLUE}TEST 4: Notification Endpoints{RESET}")
    print(f"{BLUE}{'='*80}{RESET}\n")
    
    test_endpoint("GET", "/api/notifications", "Get Notifications")
    test_endpoint("GET", "/api/notifications/count", "Notification Count")

def test_chat_endpoints():
    """Test 5: Chat endpoints"""
    print(f"\n{BLUE}{'='*80}{RESET}")
    print(f"{BLUE}TEST 5: Chat Endpoints{RESET}")
    print(f"{BLUE}{'='*80}{RESET}\n")
    
    test_endpoint("GET", "/api/chat/v2/conversations", "Chat Conversations")
    test_endpoint("GET", "/api/chat/v3/health", "Chat v3 Health")

def test_bill_endpoints():
    """Test 6: Bill endpoints"""
    print(f"\n{BLUE}{'='*80}{RESET}")
    print(f"{BLUE}TEST 6: Bill Endpoints{RESET}")
    print(f"{BLUE}{'='*80}{RESET}\n")
    
    test_endpoint("GET", "/api/bills", "List Bills")

def test_settings_endpoints():
    """Test 7: Settings endpoints"""
    print(f"\n{BLUE}{'='*80}{RESET}")
    print(f"{BLUE}TEST 7: Settings Endpoints{RESET}")
    print(f"{BLUE}{'='*80}{RESET}\n")
    
    test_endpoint("GET", "/api/settings", "Get Settings")

# ============================================
# TEST REPORT
# ============================================

def print_report():
    """Print final test report"""
    print(f"\n{'='*80}")
    print("TEST REPORT")
    print(f"{'='*80}\n")
    
    total = len(results["passed"]) + len(results["failed"]) + len(results["skipped"])
    
    print(f"{GREEN}✅ Passed: {len(results['passed'])}/{total}{RESET}")
    for test in results["passed"]:
        print(f"   - {test}")
    
    print(f"\n{RED}❌ Failed: {len(results['failed'])}/{total}{RESET}")
    for test in results["failed"]:
        print(f"   - {test}")
    
    if results["skipped"]:
        print(f"\n{YELLOW}⏭️  Skipped: {len(results['skipped'])}/{total}{RESET}")
        for test in results["skipped"]:
            print(f"   - {test}")
    
    print(f"\n{'='*80}")
    
    if len(results["failed"]) > 0:
        print(f"{RED}❌ DIAGNOSIS: Server has issues - Check logs above{RESET}")
        print(f"\nNext Steps:")
        print(f"1. Check Render logs: https://dashboard.render.com")
        print(f"2. Look for ERROR messages in the logs")
        print(f"3. Check database connection")
        print(f"4. Verify environment variables")
    else:
        print(f"{GREEN}✅ ALL TESTS PASSED - Server is healthy!{RESET}")
    
    print(f"{'='*80}\n")

# ============================================
# MAIN EXECUTION
# ============================================

if __name__ == "__main__":
    print(f"\n{'='*80}")
    print("LIFEASY V30 PRO - API DIAGNOSTIC TEST")
    print(f"{'='*80}")
    print(f"Base URL: {BASE_URL}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*80}\n")
    
    # Check if server is reachable
    try:
        response = requests.get(f"{BASE_URL}/", timeout=5)
        print(f"{GREEN}✅ Server is reachable!{RESET}\n")
    except:
        print(f"{RED}❌ WARNING: Cannot reach server at {BASE_URL}{RESET}")
        print(f"Make sure the server is running or URL is correct.\n")
        sys.exit(1)
    
    # Run all tests
    test_basic_connectivity()
    test_auth_endpoints()
    test_user_endpoints()
    test_notification_endpoints()
    test_chat_endpoints()
    test_bill_endpoints()
    test_settings_endpoints()
    
    # Print final report
    print_report()
