from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import os
import sqlite3
from threading import Thread

app = FastAPI(
    title="DynamoHive",
    version="1.0"
)

# templates
templates = Jinja2Templates(directory="backend/templates")

DB_PATH = "database/dynamohive.db"

# basit signal storage
latest_signals = []


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


def start_orchestrator():

    try:

        from backend.orchestrator import start

        print("Starting DynamoHive AI engine")

        start()

    except Exception as e:

        print("AI engine failed:", e)


@app.on_event("startup")
def startup():

    print("DynamoHive boot sequence")

    init_database()

    thread = Thread(target=start_orchestrator)
    thread.daemon = True
    thread.start()


# LANDING PAGE
@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


# HEALTH CHECK
@app.get("/health")
def health():

    return {
        "status": "ok"
    }


# SIGNAL FEED
@app.get("/signals")
def signals():

    return {
        "platform": "DynamoHive",
        "signals": latest_signals
    }
