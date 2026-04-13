"""
Create REAL tenant with actual user data
"""
import sqlite3
import hashlib

# Database connection
conn = sqlite3.connect('lifeasy_v30.db')
cursor = conn.cursor()

# Delete test tenant
cursor.execute('DELETE FROM tenants')

# Create REAL tenant with SHA256 hash (same as backend uses)
password_hash = hashlib.sha256('01042010'.encode('utf-8')).hexdigest()

cursor.execute('''
INSERT INTO tenants (email, name, phone, flat, building, is_verified, is_active, password)
VALUES (?, ?, ?, ?, ?, ?, ?, ?)
''', (
    'majadar1din@gmail.com',
    'Jewel',
    '01717574875',
    '101',
    'Building A',
    1,  # is_verified
    1,  # is_active
    password_hash
))

conn.commit()

# Verify
cursor.execute('SELECT id, name, phone, email, is_active FROM tenants')
tenant = cursor.fetchone()

print('✅ REAL tenant created successfully!')
print(f'ID: {tenant[0]}')
print(f'Name: {tenant[1]}')
print(f'Phone: {tenant[2]}')
print(f'Email: {tenant[3]}')
print(f'Active: {tenant[4]}')
print(f'\nLogin Credentials:')
print(f'Email: majadar1din@gmail.com')
print(f'Password: 01042010')

conn.close()
