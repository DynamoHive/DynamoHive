import sqlite3

conn = sqlite3.connect("dynamohive.db", check_same_thread=False)

cursor = conn.cursor()

def init_db():

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS posts (

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT,
        topic TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )

    """)

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS topics (

        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE,
        authority_score INTEGER DEFAULT 0

    )

    """)

    conn.commit()
