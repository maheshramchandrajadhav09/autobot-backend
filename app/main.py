import os
import uuid
import asyncio
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from app.ocr_worker import (
    start_mock_parse,
    get_status,
    get_result
)

# --------------------------------------------------
# APP INIT
# --------------------------------------------------

app = FastAPI(title="AutoBot Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # change later for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# STORAGE
# --------------------------------------------------

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# --------------------------------------------------
# ROUTES
# --------------------------------------------------

@app.post("/upload")
async def upload_contract_note(file: UploadFile = File(...)):
    """
    Uploads contract note and starts background parsing
    """

    upload_id = str(uuid.uuid4())
    file_path = os.path.join(
        UPLOAD_DIR,
        f"{upload_id}_{file.filename}"
    )

    # save uploaded file
    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    # start async mock parsing
    asyncio.create_task(start_mock_parse(upload_id))

    return {
        "uploadId": upload_id,
        "status": "processing"
    }


@app.get("/status/{upload_id}")
def check_status(upload_id: str):
    """
    Poll status + parsed result
    """

    return {
        "uploadId": upload_id,
        "status": get_status(upload_id),
        "result": get_result(upload_id)
    }


@app.get("/")
def health_check():
    return {"status": "AutoBot backend running"}
