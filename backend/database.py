import sqlite3

conn = sqlite3.connect("dynamohive.db", check_same_thread=False)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT,
    user_id TEXT
)
""")

conn.commit()
