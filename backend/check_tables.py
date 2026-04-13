import psycopg2

DATABASE_URL = "postgresql://lifeasy_db_user:5EtrsC4FSSM58Ovbxfuc0Bs3sYjXH622@dpg-d7bttnmuk2gs7393s3cg-a.singapore-postgres.render.com:5432/lifeasy_db?sslmode=require"

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

cursor.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public'
    ORDER BY table_name;
""")

tables = cursor.fetchall()
print("Tables in database:")
for table in tables:
    print(f"  - {table[0]}")

conn.close()
