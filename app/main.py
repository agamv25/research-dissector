import os
from fastapi import FastAPI, UploadFile, HTTPException, status
import fitz
from langchain_text_splitters import RecursiveCharacterTextSplitter
app = FastAPI(
    title="Research Paper Analysis & Summarization Engine",
    version="0.0.1",
    description="Backend API for parsing, vector indexing, and summarizing academic papers."
)

# Ensure an output directory exists for generated text files
OUTPUT_DIR = "extracted_texts"
os.makedirs(OUTPUT_DIR, exist_ok=True)

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

@app.get("/")
def read_root():
    return {
        "status": "online",
        "message": "Welcome to the Research Dissector API. System is operational."
    }

@app.post("/upload")
async def upload_pdf(file: UploadFile):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file type. Only PDF files are accepted."
        )
    try:
        contents = await file.read()  
        doc = fitz.open(stream=contents, filetype="pdf")
        
        full_text_accumulator = []
        
        for page_num, page in enumerate(doc):
            # 1. Check for tables
            tabs_finder = page.find_tables()
            if tabs_finder.tables:
                for table in tabs_finder.tables:
                    df_like_data = table.extract()
                    full_text_accumulator.append(f"\n[TABLE ON PAGE {page_num + 1}]\n{str(df_like_data)}\n")
            
            text = page.get_text("text", sort=True)
            full_text_accumulator.append(f"\n--- PAGE {page_num + 1} ---\n" + text)
        
        combined_text = "".join(full_text_accumulator)
        
        base_name = os.path.splitext(file.filename)[0]
        txt_filename = f"{base_name}_extracted.txt"
        txt_path = os.path.join(OUTPUT_DIR, txt_filename)
        
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(combined_text)
            
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap = 200,
            length_function = len,
            is_separator_regex=False,
        )
        chunks = text_splitter.create_documents([combined_text])
        print(f"Total chunks generated: {len(chunks)}")
        return {
            "filename": file.filename,
            "size_bytes": len(contents),
            "total_pages": len(doc),
            "output_txt_file": txt_path
        }
    except Exception as e:
        return {"error": str(e)}