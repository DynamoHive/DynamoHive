import sqlite3
import os
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "database", "dynamohive.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


def init_db():
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


def save_post(title, content):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO posts (title, content)
        VALUES (?, ?)
    """, (title, content))

    conn.commit()
    conn.close()


def get_posts():

    conn = get_connection()
    conn.row_factory = sqlite3.Row
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

    for row in rows:
        post = dict(row)

        # timestamp üret
        try:
            post["timestamp"] = time.mktime(
                time.strptime(post["created_at"], "%Y-%m-%d %H:%M:%S")
            )
        except:
            post["timestamp"] = time.time()

        # AI alanları
        post["keywords"] = []
        post["source"] = "internal"

        posts.append(post)

    return posts
