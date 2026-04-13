"""
LIFEASY V30 PRO - Database Connection Test
Tests PostgreSQL connection and verifies all tables exist
"""
import os
import sys
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, inspect
from datetime import datetime

# Load environment variables
load_dotenv()

# Color codes
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

print(f"\n{'='*80}")
print(f"{BLUE}LIFEASY V30 PRO - DATABASE CONNECTION TEST{RESET}")
print(f"{'='*80}\n")

# Get database URL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print(f"{RED}❌ ERROR: DATABASE_URL not set in .env file{RESET}")
    print(f"{YELLOW}Please add your PostgreSQL connection string to .env{RESET}")
    sys.exit(1)

print(f"{BLUE}📍 Database URL:{RESET} {DATABASE_URL[:60]}...")
print(f"{BLUE}📍 Environment:{RESET} {os.getenv('LIFEASY_ENV', 'development')}")
print(f"{BLUE}📍 Time:{RESET} {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

# Test connection
try:
    print(f"{BLUE}🔌 Testing database connection...{RESET}")
    engine = create_engine(DATABASE_URL)
    
    with engine.connect() as conn:
        # Test basic connection
        result = conn.execute(text("SELECT 1"))
        print(f"{GREEN}✅ Database connection successful!{RESET}\n")
        
        # Get database info
        print(f"{BLUE}📊 Database Information:{RESET}")
        result = conn.execute(text("""
            SELECT current_database(), current_user, version()
        """))
        row = result.fetchone()
        print(f"   Database: {row[0]}")
        print(f"   User: {row[1]}")
        print(f"   PostgreSQL Version: {row[2][:50]}...\n")
        
        # Check tables
        print(f"{BLUE}📋 Checking Tables...{RESET}")
        result = conn.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """))
        tables = [row[0] for row in result.fetchall()]
        
        if tables:
            print(f"{GREEN}✅ Found {len(tables)} tables:{RESET}\n")
            for table in tables:
                # Get row count
                try:
                    count_result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                    row_count = count_result.fetchone()[0]
                    print(f"   ✅ {table:30s} - {row_count:5d} rows")
                except:
                    print(f"   ⚠️  {table:30s} - Error counting rows")
        else:
            print(f"{RED}❌ No tables found in database!{RESET}")
            print(f"{YELLOW}You need to run database migration.{RESET}\n")
            
            # Ask if user wants to create tables
            response = input(f"{YELLOW}Create tables now? (y/n): {RESET}").lower()
            if response == 'y':
                print(f"\n{BLUE}Creating tables...{RESET}")
                try:
                    from database_prod import Base
                    from models import *  # Import all models
                    
                    Base.metadata.create_all(engine)
                    print(f"{GREEN}✅ Tables created successfully!{RESET}")
                    
                    # Verify
                    result = conn.execute(text("""
                        SELECT table_name 
                        FROM information_schema.tables 
                        WHERE table_schema = 'public'
                    """))
                    tables = [row[0] for row in result.fetchall()]
                    print(f"{GREEN}✅ Verified: {len(tables)} tables now exist{RESET}")
                except Exception as e:
                    print(f"{RED}❌ Failed to create tables: {e}{RESET}")
                    print(f"{YELLOW}Try running: python create_all_tables.py{RESET}")
        
        # Check for specific critical tables
        print(f"\n{BLUE}🔍 Verifying Critical Tables...{RESET}")
        required_tables = [
            'tenants', 'otp_codes', 'payments', 'notifications',
            'chat_messages', 'conversations', 'bills', 'settings'
        ]
        
        missing_tables = []
        for table in required_tables:
            if table in tables:
                print(f"   ✅ {table}")
            else:
                print(f"   ❌ {table} - MISSING")
                missing_tables.append(table)
        
        if missing_tables:
            print(f"\n{RED}⚠️  Missing {len(missing_tables)} critical tables:{RESET}")
            for table in missing_tables:
                print(f"   - {table}")
            print(f"\n{YELLOW}Run: python create_all_tables.py{RESET}")
        else:
            print(f"\n{GREEN}✅ All critical tables present!{RESET}")
        
        # Check tenant data
        print(f"\n{BLUE}👥 Checking Tenant Data...{RESET}")
        try:
            result = conn.execute(text("SELECT COUNT(*) FROM tenants"))
            count = result.fetchone()[0]
            print(f"   Total tenants: {count}")
            
            if count > 0:
                result = conn.execute(text("""
                    SELECT id, full_name, email, is_approved 
                    FROM tenants 
                    LIMIT 5
                """))
                print(f"\n{BLUE}   Sample tenants:{RESET}")
                for row in result.fetchall():
                    status = "✅" if row[3] else "⏳"
                    print(f"   {status} ID: {row[0]}, Name: {row[1]}, Email: {row[2]}")
        except Exception as e:
            print(f"   ⚠️  Could not query tenants: {e}")
        
        # Check for pending approvals
        try:
            result = conn.execute(text("""
                SELECT COUNT(*) FROM tenants WHERE is_approved = false
            """))
            pending = result.fetchone()[0]
            if pending > 0:
                print(f"\n{YELLOW}⏳ {pending} tenants pending approval{RESET}")
        except:
            pass
        
        print(f"\n{'='*80}")
        print(f"{GREEN}✅ DATABASE TEST COMPLETED SUCCESSFULLY{RESET}")
        print(f"{'='*80}\n")

except Exception as e:
    print(f"\n{RED}❌ DATABASE CONNECTION FAILED!{RESET}")
    print(f"\n{BLUE}Error Type:{RESET} {type(e).__name__}")
    print(f"{BLUE}Error Message:{RESET} {str(e)}\n")
    
    print(f"{YELLOW}Possible causes:{RESET}")
    print(f"   1. DATABASE_URL is incorrect")
    print(f"   2. PostgreSQL server is not running")
    print(f"   3. Database credentials are wrong")
    print(f"   4. Network/firewall blocking connection")
    print(f"   5. Render database is deleted/inactive")
    
    print(f"\n{YELLOW}Troubleshooting steps:{RESET}")
    print(f"   1. Check DATABASE_URL in .env file")
    print(f"   2. Verify Render PostgreSQL is active")
    print(f"   3. Test connection from Render Shell")
    print(f"   4. Check database credentials")
    print(f"   5. Look at Render logs for details")
    
    print(f"\n{'='*80}\n")
    
    sys.exit(1)
