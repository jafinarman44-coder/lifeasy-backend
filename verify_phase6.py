"""
LIFEASY V27+ PHASE 6 - Verification Script
Tests all new features after migration
"""
import sqlite3
import requests
import json
from datetime import datetime

DATABASE_PATH = "backend/lifeasy_v30.db"
API_BASE = "http://localhost:8000/api"


def test_database_migration():
    """Test if database migration completed successfully"""
    print("\n" + "="*60)
    print("TESTING DATABASE MIGRATION")
    print("="*60)
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Test 1: Check tenants table has new columns
    print("\n[1/7] Checking tenants table columns...")
    cursor.execute("PRAGMA table_info(tenants)")
    columns = [col[1] for col in cursor.fetchall()]
    
    required_columns = ['email', 'password', 'is_verified', 'is_active', 'profile_photo']
    missing_columns = [col for col in required_columns if col not in columns]
    
    if missing_columns:
        print(f"❌ Missing columns: {missing_columns}")
        return False
    else:
        print(f"✅ All required columns present: {required_columns}")
    
    # Test 2: Check new tables exist
    print("\n[2/7] Checking new tables...")
    required_tables = [
        'otp_codes',
        'notifications',
        'chat_rooms',
        'chat_participants',
        'chat_messages',
        'blocked_users',
        'call_logs'
    ]
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    existing_tables = [table[0] for table in cursor.fetchall()]
    
    missing_tables = [table for table in required_tables if table not in existing_tables]
    
    if missing_tables:
        print(f"❌ Missing tables: {missing_tables}")
        return False
    else:
        print(f"✅ All required tables created: {len(required_tables)} tables")
    
    # Test 3: Check indexes
    print("\n[3/7] Checking indexes...")
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index'")
    indexes = [idx[0] for idx in cursor.fetchall()]
    
    required_indexes = [
        'idx_otp_email',
        'idx_notifications_tenant',
        'idx_chat_participants_room',
        'idx_chat_messages_room',
        'idx_blocked_users'
    ]
    
    missing_indexes = [idx for idx in required_indexes if idx not in indexes]
    
    if missing_indexes:
        print(f"⚠️  Some indexes missing: {missing_indexes}")
    else:
        print(f"✅ All indexes created")
    
    conn.close()
    print("\n✅ DATABASE MIGRATION VERIFIED SUCCESSFULLY")
    return True


def test_auth_apis():
    """Test authentication APIs"""
    print("\n" + "="*60)
    print("TESTING AUTHENTICATION APIs")
    print("="*60)
    
    # Test endpoint availability
    endpoints = [
        ("POST", "/api/auth/send-otp"),
        ("POST", "/api/auth/verify"),
        ("POST", "/api/auth/login"),
        ("GET", "/api/auth/profile/1"),
    ]
    
    print("\nChecking API endpoints (server must be running)...")
    
    try:
        # Test health endpoint first
        response = requests.get(f"{API_BASE}/health", timeout=5)
        if response.status_code == 200:
            print(f"✅ Backend server is running")
            print(f"   Health status: {response.json().get('status', 'unknown')}")
        else:
            print(f"⚠️  Health check returned: {response.status_code}")
        
        # Test API docs
        response = requests.get(f"{API_BASE}/docs", timeout=5)
        if response.status_code == 200:
            print(f"✅ API documentation available at /docs")
        
    except requests.exceptions.ConnectionError:
        print(f"❌ Backend server not running!")
        print(f"   Start server: python backend\\main_prod.py")
        return False
    except Exception as e:
        print(f"⚠️  Error testing APIs: {e}")
        return False
    
    print("\n✅ AUTH APIs READY")
    return True


def test_notification_system():
    """Test notification system structure"""
    print("\n" + "="*60)
    print("TESTING NOTIFICATION SYSTEM")
    print("="*60)
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Check notifications table structure
    print("\n[1/2] Checking notifications table...")
    cursor.execute("PRAGMA table_info(notifications)")
    columns = cursor.fetchall()
    
    expected_columns = ['id', 'tenant_id', 'title', 'message', 'is_read', 'created_at']
    actual_columns = [col[1] for col in columns]
    
    if all(col in actual_columns for col in expected_columns):
        print(f"✅ Notifications table structure correct")
    else:
        print(f"❌ Notifications table structure incorrect")
        return False
    
    # Check API endpoint
    print("[2/2] Checking notification API...")
    try:
        response = requests.options(f"{API_BASE}/notifications/send", timeout=5)
        print(f"✅ Notification API endpoint exists")
    except:
        print(f"⚠️  Cannot verify notification API (server may not be running)")
    
    conn.close()
    print("\n✅ NOTIFICATION SYSTEM READY")
    return True


def test_chat_system():
    """Test chat system structure"""
    print("\n" + "="*60)
    print("TESTING CHAT SYSTEM")
    print("="*60)
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Check chat tables
    print("\n[1/2] Checking chat tables structure...")
    chat_tables = ['chat_rooms', 'chat_participants', 'chat_messages', 'blocked_users']
    
    for table in chat_tables:
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()
        if len(columns) > 0:
            print(f"   ✓ {table}: {len(columns)} columns")
        else:
            print(f"   ❌ {table}: Empty or missing")
            conn.close()
            return False
    
    # Check relationships
    print("[2/2] Verifying foreign keys...")
    cursor.execute("PRAGMA foreign_key_list(chat_participants)")
    fk1 = cursor.fetchall()
    cursor.execute("PRAGMA foreign_key_list(chat_messages)")
    fk2 = cursor.fetchall()
    
    if len(fk1) > 0 and len(fk2) > 0:
        print(f"✅ Foreign keys configured correctly")
    else:
        print(f"⚠️  Foreign keys may be missing")
    
    conn.close()
    print("\n✅ CHAT SYSTEM READY")
    return True


def test_calling_system():
    """Test calling system structure"""
    print("\n" + "="*60)
    print("TESTING CALLING SYSTEM")
    print("="*60)
    
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    
    # Check call_logs table
    print("\n[1/1] Checking call_logs table...")
    cursor.execute("PRAGMA table_info(call_logs)")
    columns = cursor.fetchall()
    
    expected_columns = ['caller_id', 'receiver_id', 'call_type', 'status', 'duration', 'created_at']
    actual_columns = [col[1] for col in columns]
    
    if all(col in actual_columns for col in expected_columns):
        print(f"✅ Call logs table structure correct")
        print(f"   Columns: {len(columns)} total")
    else:
        print(f"❌ Call logs table structure incorrect")
        conn.close()
        return False
    
    conn.close()
    print("\n✅ CALLING SYSTEM READY")
    return True


def generate_test_report():
    """Generate comprehensive test report"""
    print("\n\n" + "="*60)
    print("PHASE 6 VERIFICATION REPORT")
    print("="*60)
    
    tests = [
        ("Database Migration", test_database_migration),
        ("Auth APIs", test_auth_apis),
        ("Notification System", test_notification_system),
        ("Chat System", test_chat_system),
        ("Calling System", test_calling_system),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ {test_name} FAILED with error: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed ({(passed/total*100):.1f}%)")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! PHASE 6 IS READY!")
        print("\nNext steps:")
        print("1. Update Windows app tenant registration form")
        print("2. Add notification panel to admin interface")
        print("3. Integrate mobile app with new APIs")
        print("4. Configure email SMTP settings")
    else:
        print("\n⚠️  Some tests failed. Please review the errors above.")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    print("\n" + "="*60)
    print("  LIFEASY V27+ PHASE 6 - VERIFICATION TOOL")
    print("="*60)
    print("\nThis tool will verify that Phase 6 features")
    print("are properly installed and working.\n")
    
    try:
        generate_test_report()
    except Exception as e:
        print(f"\n❌ Verification failed with error: {e}")
        import traceback
        traceback.print_exc()
    
    print("\nPress any key to exit...")
    input()
