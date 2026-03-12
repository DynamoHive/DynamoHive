from fastapi import FastAPI
import os
import sqlite3

app = FastAPI(title="DynamoHive", version="1.0")

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


@app.on_event("startup")
def startup():
    init_database()


@app.get("/")
def root():
    return {
        "platform": "DynamoHive",
        "status": "running"
    }


@app.get("/health")
def health():
    return {"status": "ok"}

