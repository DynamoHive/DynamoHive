import sqlite3
import os
import time

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_DIR = os.path.join(BASE_DIR, "database")
DB_PATH = os.path.join(DB_DIR, "dynamohive.db")


def init_db():

    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)

    conn = sqlite3.connect(DB_PATH)
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


def get_connection():
    init_db()
    return sqlite3.connect(DB_PATH)


def save_post(title, content):

    try:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO posts (title, content)
            VALUES (?, ?)
        """, (title, content))

        conn.commit()
        conn.close()

    except Exception as e:
        print("DB write error:", e)


def get_posts():

    try:
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

            try:
                post["timestamp"] = time.mktime(
                    time.strptime(post["created_at"], "%Y-%m-%d %H:%M:%S")
                )
            except:
                post["timestamp"] = time.time()

            post["keywords"] = []
            post["source"] = "internal"

            posts.append(post)

        return posts

    except Exception as e:
        print("DB read error:", e)
        return []
