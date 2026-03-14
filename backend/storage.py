import sqlite3
import os

DB_PATH = "database/dynamohive.db"


def get_connection():
    os.makedirs("database", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_posts_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS posts ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "title TEXT,"
        "content TEXT,"
        "created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
    )

    conn.commit()
    conn.close()


def get_posts():
    init_posts_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id,title,content,created_at "
        "FROM posts "
        "ORDER BY created_at DESC "
        "LIMIT 50"
    )

    rows = cursor.fetchall()
    conn.close()

    return [
        {
            "id": r["id"],
            "title": r["title"],
            "content": r["content"],
            "created_at": r["created_at"]
        }
        for r in rows
    ]
