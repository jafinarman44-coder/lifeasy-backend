"""
Check Tenants Table Schema
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

print("\nChecking tenants table schema...\n")

with engine.connect() as conn:
    # Get columns
    result = conn.execute(text("""
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_name = 'tenants'
        ORDER BY ordinal_position
    """))
    
    print("Columns in 'tenants' table:")
    print("-" * 60)
    for row in result.fetchall():
        nullable = "NULL" if row[2] == 'YES' else "NOT NULL"
        print(f"  {row[0]:25s} {row[1]:20s} {nullable}")
    
    # Get actual data
    print("\n\nActual tenant data:")
    print("-" * 60)
    result = conn.execute(text("SELECT * FROM tenants"))
    columns = result.keys()
    print(f"Columns: {', '.join(columns)}\n")
    
    for row in result.fetchall():
        print(f"Tenant ID: {row[0]}")
        for i, col in enumerate(columns):
            print(f"  {col}: {row[i]}")
        print()
