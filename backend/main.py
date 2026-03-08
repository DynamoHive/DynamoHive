from importlib import import_module

app = FastAPI()

ai_module = import_module("ai-engine.recommendation")

@app.get("/")
def home():
    return {"platform": "DynamoHive", "status": "running"}

@app.get("/feed")
def get_feed(user_id: int = 1):
