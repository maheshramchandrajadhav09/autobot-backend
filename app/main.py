import os
import uuid
import asyncio
from datetime import datetime

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

# -------------------------------
# OCR / CONTRACT NOTE (existing)
# -------------------------------
from app.ocr_worker import (
    start_mock_parse,
    get_status,
    get_result
)

# -------------------------------
# AUTOBOT PHASE-A IMPORTS
# -------------------------------
from app.core.bot_state import BOT_STATE
from app.core.decision_engine import run_autobot_cycle

# --------------------------------------------------
# APP INIT
# --------------------------------------------------

app = FastAPI(title="AutoBot Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten later
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
# CONTRACT NOTE ROUTES (UNCHANGED LOGIC)
# --------------------------------------------------

@app.post("/upload")
async def upload_contract_note(file: UploadFile = File(...)):
    """
    Upload contract note PDF and start background parsing
    """

    upload_id = str(uuid.uuid4())
    file_path = os.path.join(
        UPLOAD_DIR,
        f"{upload_id}_{file.filename}"
    )

    contents = await file.read()
    with open(file_path, "wb") as f:
        f.write(contents)

    # async OCR / parsing
    asyncio.create_task(start_mock_parse(upload_id))

    return {
        "uploadId": upload_id,
        "status": "processing"
    }


@app.get("/status/{upload_id}")
def check_status(upload_id: str):
    """
    Poll contract note parsing status
    """

    return {
        "uploadId": upload_id,
        "status": get_status(upload_id),
        "result": get_result(upload_id)
    }

# --------------------------------------------------
# AUTOBOT PHASE-A ROUTES
# --------------------------------------------------

@app.post("/api/v1/bot/start")
def start_autobot():
    """
    Start autonomous Phase-A bot cycle (paper trading)
    """
    BOT_STATE["status"] = "RUNNING"
    run_autobot_cycle()

    return {
        "message": "AutoBot started",
        "status": BOT_STATE["status"],
        "started_at": datetime.utcnow()
    }


@app.get("/api/v1/bot/status")
def autobot_status():
    """
    Returns current bot state for Android UI
    """
    return BOT_STATE


@app.post("/api/v1/bot/stop")
def stop_autobot():
    BOT_STATE["status"] = "PAUSED"
    return {
        "message": "AutoBot paused",
        "status": BOT_STATE["status"]
    }

# --------------------------------------------------
# HEALTH
# --------------------------------------------------

@app.get("/")
def health_check():
    return {"status": "AutoBot backend running"}
