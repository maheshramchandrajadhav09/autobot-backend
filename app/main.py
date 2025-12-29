from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uuid
import os
import asyncio
from app.ocr_worker import start_mock_parse, get_status, get_result

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload")
async def upload_contract_note(file: UploadFile = File(...)):
    upload_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{upload_id}_{file.filename}")

    with open(file_path, "wb") as f:
        f.write(await file.read())

    asyncio.create_task(start_mock_parse(upload_id))

    return {
        "uploadId": upload_id,
        "status": "processing"
    }

@app.get("/status/{upload_id}")
def check_status(upload_id: str):
    return {
        "uploadId": upload_id,
        "status": get_status(upload_id),
        "result": get_result(upload_id)
    }

