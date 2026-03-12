from fastapi import FastAPI
from database.database import init_database

app = FastAPI(
    title="DynamoHive",
    description="Autonomous Intelligence Platform",
    version="1.0"
)


@app.on_event("startup")
async def startup_event():
    # veritabanını başlat
    init_database()


@app.get("/")
def root():
    return {
        "platform": "DynamoHive",
        "status": "running",
        "message": "DynamoHive AI system is active"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }
