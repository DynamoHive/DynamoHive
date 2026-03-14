import sqlite3

DB_PATH = "database/dynamohive.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def get_cursor():
    conn = get_connection()
    return conn, conn.cursor()
