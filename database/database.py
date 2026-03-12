import sqlite3

# Database connection
conn = sqlite3.connect("database.db", check_same_thread=False)

# Global cursor
cursor = conn.cursor()

# Function to get new cursor
def get_cursor():
    return conn.cursor()
