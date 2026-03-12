from fastapi import FastAPI
from database.database import init_database

app = FastAPI(
    title="DynamoHive",
    version="1.0"
)

@app.on_event("startup")
def startup():
    init_database()

@app.get("/")
def root():
    return {"status": "DynamoHive running"}
