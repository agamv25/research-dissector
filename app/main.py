from fastapi import FastAPI
import redis
import os

app = FastAPI(
    title="Research Paper Analysis & Summarization Engine",
    version="0.0.1",
    description="Backend API for parsing, vector indexing, and summarizing academic papers."
)
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.Redis.from_url(REDIS_URL)

@app.get("/")
def read_root():
    return{
        "status": "online",
        "message": "Welcome to the Research Dissector API. System is operational."
    }

@app.get("/health/redis")
def check_redis():
    try:
        redis_client.ping()
        return {"redis": "connected"}
    except Exception as e:
        return {"redis": "disconnected", "error": str(e)}