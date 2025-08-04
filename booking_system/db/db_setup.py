import sqlite3
import os

db_folder = os.path.join(os.path.dirname(__file__), 'db')
os.makedirs(db_folder, exist_ok=True)
db_path = os.path.join(db_folder, 'database.db')

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        room_number INTEGER NOT NULL,
        date TEXT NOT NULL,
        time TEXT NOT NULL,
        user_name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL
    )
''')

conn.commit()
conn.close()
print("📦 База данных инициализирована.")
