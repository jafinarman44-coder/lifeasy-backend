import sqlite3

conn = sqlite3.connect('lifeasy_v30.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS chat_presence (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    status TEXT DEFAULT 'offline',
    last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    building_id INTEGER,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
''')

conn.commit()
print('✅ chat_presence table created')
conn.close()
