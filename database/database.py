import sqlite3

conn = None


def init_database():

    global conn

    conn = sqlite3.connect("dynamohive.db", check_same_thread=False)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS posts(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        content TEXT
    )
    """)

    conn.commit()


def get_posts():

    cursor = conn.cursor()

    cursor.execute("SELECT id,title,content FROM posts ORDER BY id DESC")

    return cursor.fetchall()


def get_post(post_id):

    cursor = conn.cursor()

    cursor.execute(
        "SELECT id,title,content FROM posts WHERE id=?",
        (post_id,)
    )

    return cursor.fetchone()


def save_post(title, content):

    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO posts(title,content) VALUES(?,?)",
        (title, content)
    )

    conn.commit()

