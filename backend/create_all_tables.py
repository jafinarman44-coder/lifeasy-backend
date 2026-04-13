"""
Create all tables in Render PostgreSQL database
"""
import psycopg2
import hashlib

DATABASE_URL = "postgresql://lifeasy_db_user:5EtrsC4FSSM58Ovbxfuc0Bs3sYjXH622@dpg-d7bttnmuk2gs7393s3cg-a.singapore-postgres.render.com:5432/lifeasy_db?sslmode=require"

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

print("Creating all tables...")

# Create tenants table
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
print("✅ tenants table created")

# Create otp_codes table
cursor.execute('''
CREATE TABLE IF NOT EXISTS otp_codes (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255),
    otp VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    is_used BOOLEAN DEFAULT FALSE,
    name VARCHAR(255),
    phone VARCHAR(50),
    password VARCHAR(255)
)
''')
print("✅ otp_codes table created")

# Create chat_presence table
cursor.execute('''
CREATE TABLE IF NOT EXISTS chat_presence (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    status VARCHAR(50) DEFAULT 'offline',
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    building_id INTEGER,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
print("✅ chat_presence table created")

# Create bills table
cursor.execute('''
CREATE TABLE IF NOT EXISTS bills (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER,
    amount DECIMAL(10,2),
    due_date DATE,
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
print("✅ bills table created")

# Create payments table
cursor.execute('''
CREATE TABLE IF NOT EXISTS payments (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER,
    amount DECIMAL(10,2),
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
print("✅ payments table created")

# Create notifications table
cursor.execute('''
CREATE TABLE IF NOT EXISTS notifications (
    id SERIAL PRIMARY KEY,
    tenant_id INTEGER,
    message TEXT,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
print("✅ notifications table created")

# Create chat_rooms table
cursor.execute('''
CREATE TABLE IF NOT EXISTS chat_rooms (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    type VARCHAR(50),
    building_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
print("✅ chat_rooms table created")

# Create chat_participants table
cursor.execute('''
CREATE TABLE IF NOT EXISTS chat_participants (
    id SERIAL PRIMARY KEY,
    room_id INTEGER,
    user_id INTEGER,
    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
print("✅ chat_participants table created")

# Create chat_messages table
cursor.execute('''
CREATE TABLE IF NOT EXISTS chat_messages (
    id SERIAL PRIMARY KEY,
    room_id INTEGER,
    sender_id INTEGER,
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
print("✅ chat_messages table created")

# Create blocked_users table
cursor.execute('''
CREATE TABLE IF NOT EXISTS blocked_users (
    id SERIAL PRIMARY KEY,
    user_id INTEGER,
    blocked_user_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
print("✅ blocked_users table created")

# Create call_logs table
cursor.execute('''
CREATE TABLE IF NOT EXISTS call_logs (
    id SERIAL PRIMARY KEY,
    caller_id INTEGER,
    receiver_id INTEGER,
    duration INTEGER,
    status VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
print("✅ call_logs table created")

# Create chat_typing table
cursor.execute('''
CREATE TABLE IF NOT EXISTS chat_typing (
    id SERIAL PRIMARY KEY,
    room_id INTEGER,
    user_id INTEGER,
    is_typing BOOLEAN DEFAULT FALSE,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
print("✅ chat_typing table created")

# Create chat_unread table
cursor.execute('''
CREATE TABLE IF NOT EXISTS chat_unread (
    id SERIAL PRIMARY KEY,
    room_id INTEGER,
    user_id INTEGER,
    count INTEGER DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')
print("✅ chat_unread table created")

# Insert tenant
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
print("\n✅ Tenant created successfully!")

# Verify
cursor.execute('SELECT id, name, email, is_active FROM tenants WHERE email = %s', ('majadar1din@gmail.com',))
tenant = cursor.fetchone()
print(f"\nTenant Details:")
print(f"ID: {tenant[0]}")
print(f"Name: {tenant[1]}")
print(f"Email: {tenant[2]}")
print(f"Active: {tenant[3]}")

conn.close()
print("\n✅ All tables created and tenant ready!")
