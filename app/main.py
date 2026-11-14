from fastapi import FastAPI
import redis
import os
from fastapi import UploadFile
from fastapi import HTTPException, status
import pymupdf

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

@app.post("/upload")
async def upload_pdf(file: UploadFile):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only PDF files are accepted."
        )
    
    try:
        contents = await file.read()  
        doc = pymupdf.open(stream=contents, filetype="pdf")
        for page in doc:
            text = page.get_text("text", sort=True)
            print(text)
        return {
            "filename": file.filename,
            "size_bytes": len(contents)
        }
    except Exception as e:
        return {"error": str(e)}