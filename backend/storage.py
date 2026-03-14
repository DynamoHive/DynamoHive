import sqlite3
import os

# Veritabanı yolu
DB_PATH = "database/dynamohive.db"


def get_connection():
    """
    SQLite bağlantısı oluşturur.
    """
    os.makedirs("database", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    return conn


def ensure_posts_table():
    """
    posts tablosu yoksa oluşturur.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()


def get_posts():
    """
    Son 50 postu döndürür.
    """

    ensure_posts_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, content, created_at
        FROM posts
        ORDER BY created_at DESC
        LIMIT 50
    """)

    rows = cursor.fetchall()

    conn.close()

    posts = []

    for r in rows:

        posts.append({
            "id": r["id"],
            "title": r["title"],
            "content": r["content"],
            "created_at": r["created_at"]
        })

    return posts


def save_post(title, content):
    """
    Yeni post kaydeder.
    """

    ensure_posts_table()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO posts (title, content)
        VALUES (?, ?)
    """, (title, content))

    conn.commit()
    conn.close()
