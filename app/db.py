import os
from dotenv import load_dotenv
import psycopg2
from psycopg2 import OperationalError

load_dotenv()

db_url = os.getenv("DATABASE_URL")
if not db_url:
    raise RuntimeError("DATABASE_URL is not set in environment or .env file.")

def get_connection():
    try:
        conn = psycopg2.connect(
            db_url
        )
        return conn
    except OperationalError as e:
        print(f"Database connection failed: {e}")
        raise

def insert_paper_chunks(filename: str, chunks: list[str], embeddings: list[list[float]]) -> int:
    if len(chunks) != len(embeddings): raise ValueError("Chunks and embeddings must have the same length.")
    if not chunks:
        return 0
