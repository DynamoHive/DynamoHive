from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"platform": "DynamoHive", "status": "running"}

@app.get("/feed")
def get_feed():
    return {
        "posts": [
            {"id": 1, "content": "Welcome to DynamoHive"},
            {"id": 2, "content": "AI powered creator platform"}
        ]
    }
DynamoHive
DynamoHive
Repository navigation
Code
Issues
Pull requests
Actions
Projects
Wiki
Security
Insights
Settings
Files
Go to file
t
ai-engine
backend
backend
main.py
users.py
README.md
main.py
database
frontend
system-core.json
DynamoHive/backend
/backend/
DynamoHive
DynamoHive
Create users.py
268c502
 · 
7 minutes ago
Name	Last commit message	Last commit date
..
main.py
Create main.py
5 hours ago
users.py
Create users.py
7 minutes ag
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"platform": "DynamoHive", "status": "running"}

@app.get("/feed")
def get_feed():
    return {
        "posts": [
            {"id": 1, "content": "Welcome to DynamoHive"},
            {"id": 2, "content": "AI powered creator platform"}
        ]
    }
