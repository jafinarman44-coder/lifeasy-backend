import sqlite3
import os

# Find the correct database file
db_files = ['lifeasy_v30.db', 'lifeasy_v28.db', 'lifeasy.db']
db_file = None

for f in db_files:
    if os.path.exists(f):
        db_file = f
        break

if not db_file:
    print("❌ No database found!")
    exit()

print(f"Using database: {db_file}")

conn = sqlite3.connect(db_file)
cursor = conn.cursor()

try:
    cursor.execute('ALTER TABLE otp_codes ADD COLUMN is_password_reset BOOLEAN DEFAULT 0')
    conn.commit()
    print('✅ Column is_password_reset added successfully!')
except Exception as e:
    print(f'ℹ️ Column may already exist: {e}')

conn.close()
