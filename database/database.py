import sqlite3
import os

DB_PATH = "database/dynamohive.db"

def init_database():

    os.makedirs("database", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS system_state (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        status TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()
