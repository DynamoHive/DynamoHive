import sqlite3
import os

DB_PATH = "database/dynamohive.db"


def get_connection():

    os.makedirs("database", exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    return conn
