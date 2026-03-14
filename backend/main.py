from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import os
import sqlite3
from threading import Thread

app = FastAPI(
    title="DynamoHive",
    version="1.0"
)

# -------------------------------
# PATHS
# -------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_PATH = os.path.join(BASE_DIR, "templates")
STATIC_PATH = os.path.join(BASE_DIR, "static")
DB_DIR = os.path.join(BASE_DIR, "..", "database")
DB_PATH = os.path.join(DB_DIR, "dynamohive.db")

# -------------------------------
# TEMPLATES
# -------------------------------

templates = Jinja2Templates(directory=TEMPLATES_PATH)

# -------------------------------
# STATIC FILES
# -------------------------------

os.makedirs(STATIC_PATH, exist_ok=True)

app.mount(
    "/static",
    StaticFiles(directory=STATIC_PATH),
    name="static"
)

# -------------------------------
# DATABASE
# -------------------------------

def init_database():

    os.makedirs(DB_DIR, exist_ok=True)

    conn = sqlite3.connect(DB_PATH, check_same_thread=False)

    try:

        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS system_state (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            status TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        conn.commit()

    finally:
        conn.close()

# -------------------------------
# AI ENGINE
# -------------------------------

def start_orchestrator():

    try:

        from orchestrator import start

        print("Starting DynamoHive AI engine")

        start()

    except Exception as e:

        print("AI engine failed:", e)

# -------------------------------
# STARTUP
# -------------------------------

@app.on_event("startup")
def startup():

    print("DynamoHive boot sequence")

    init_database()

    thread = Thread(
        target=start_orchestrator,
        daemon=True,
        name="dynamohive-orchestrator"
    )

    thread.start()

# -------------------------------
# LANDING PAGE
# -------------------------------

@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )

# -------------------------------
# DASHBOARD
# -------------------------------

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request}
    )

# -------------------------------
# FEED PAGE
# -------------------------------

@app.get("/feed", response_class=HTMLResponse)
def feed_page(request: Request):

    return templates.TemplateResponse(
        "feed.html",
        {"request": request}
    )

# -------------------------------
# ABOUT PAGE
# -------------------------------

@app.get("/about", response_class=HTMLResponse)
def about(request: Request):

    return templates.TemplateResponse(
        "about.html",
        {"request": request}
    )

# -------------------------------
# HEALTH CHECK
# -------------------------------

@app.get("/health")
def health():

    return {
        "platform": "DynamoHive",
        "status": "running"
    }

# -------------------------------
# SIGNAL API
# -------------------------------

@app.get("/signals")
def signals():

    from ai_engine.signal_radar import get_latest_signals

    signals = get_latest_signals()

    return {
        "platform": "DynamoHive",
        "signals": signals
    }

# -------------------------------
# NEWS FEED API
# -------------------------------

@app.get("/api/feed")
def feed_api():

    from storage import get_posts

    posts = get_posts()

    return {
        "platform": "DynamoHive",
        "feed": posts
    }
