import sqlite3

conn = sqlite3.connect("database.db", check_same_thread=False)

def get_cursor():
    return conn.cursor()
