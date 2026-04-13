"""
Update Render database with tenant data
"""
import psycopg2
import hashlib

# Render PostgreSQL connection
DATABASE_URL = "postgresql://lifeasy_db_user:5EtrsC4FSSM58Ovbxfuc0Bs3sYjXH622@dpg-d7bttnmuk2gs7393s3cg-a.singapore-postgres.render.com:5432/lifeasy_db?sslmode=require"

# Connect to database
conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# Create tenants table if not exists
cursor.execute('''
CREATE TABLE IF NOT EXISTS tenants (
    id SERIAL PRIMARY KEY,
    tenant_id VARCHAR(255) UNIQUE,
    name VARCHAR(255) NOT NULL,
    phone VARCHAR(50),
    flat VARCHAR(50),
    building VARCHAR(255),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    avatar_url TEXT,
    is_verified BOOLEAN DEFAULT FALSE,
    is_active BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

print("✅ Tenants table created")

# Create real tenant
password_hash = hashlib.sha256('01042010'.encode('utf-8')).hexdigest()

cursor.execute('''
INSERT INTO tenants (email, name, phone, flat, building, is_verified, is_active, password)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
ON CONFLICT (email) DO UPDATE SET
    name = EXCLUDED.name,
    phone = EXCLUDED.phone,
    flat = EXCLUDED.flat,
    building = EXCLUDED.building,
    is_verified = EXCLUDED.is_verified,
    is_active = EXCLUDED.is_active,
    password = EXCLUDED.password
''', (
    'majadar1din@gmail.com',
    'Jewel',
    '01717574875',
    '101',
    'Building A',
    True,
    True,
    password_hash
))

conn.commit()

# Verify
cursor.execute('SELECT id, name, phone, email, is_active FROM tenants WHERE email = %s', ('majadar1din@gmail.com',))
tenant = cursor.fetchone()

print('✅ REAL tenant created in Render database!')
print(f'ID: {tenant[0]}')
print(f'Name: {tenant[1]}')
print(f'Phone: {tenant[2]}')
print(f'Email: {tenant[3]}')
print(f'Active: {tenant[4]}')

cursor.execute('SELECT COUNT(*) FROM tenants')
count = cursor.fetchone()[0]
print(f'\nTotal tenants in database: {count}')

conn.close()
