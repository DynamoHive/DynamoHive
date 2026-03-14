from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import os
from threading import Thread

from backend.storage import get_posts


app = FastAPI(
    title="DynamoHive",
    version="1.0"
)

# -------------------------
# TEMPLATES
# -------------------------

templates = Jinja2Templates(directory="backend/templates")

# -------------------------
# STATIC FILES
# -------------------------

STATIC_PATH = "backend/static"
os.makedirs(STATIC_PATH, exist_ok=True)

app.mount(
    "/static",
    StaticFiles(directory=STATIC_PATH),
    name="static"
)

# -------------------------
# DATABASE INIT
# -------------------------

DB_PATH = "database/dynamohive.db"


def init_database():

    os.makedirs("database", exist_ok=True)

    import sqlite3

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


# -------------------------
# AI ENGINE
# -------------------------

def start_orchestrator():

    try:

        from backend.orchestrator import start

        print("Starting DynamoHive AI engine")

        start()

    except Exception as e:

        print("AI engine failed:", e)


# -------------------------
# STARTUP
# -------------------------

@app.on_event("startup")
def startup():

    print("DynamoHive boot sequence")

    init_database()

    thread = Thread(target=start_orchestrator, daemon=True)
    thread.start()


# -------------------------
# LANDING PAGE
# -------------------------

@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


# -------------------------
# DASHBOARD
# -------------------------

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request}
    )


# -------------------------
# FEED PAGE
# -------------------------

@app.get("/feed", response_class=HTMLResponse)
def feed_page(request: Request):

    return templates.TemplateResponse(
        "feed.html",
        {"request": request}
    )


# -------------------------
# API FEED
# -------------------------

@app.get("/api/feed")
def feed_api():

    posts = get_posts()

    return {
        "platform": "DynamoHive",
        "feed": posts
    }


# -------------------------
# HEALTH CHECK
# -------------------------

@app.get("/health")
def health():

    return {"status": "ok"}
