from fastapi import APIRouter
from core.bot_state import BOT_STATE
from core.decision_engine import run_autobot_cycle

router = APIRouter(prefix="/api/v1/bot", tags=["Bot"])

@router.post("/start")
def start_bot():
    run_autobot_cycle()
    return {"status": "started"}

@router.get("/status")
def bot_status():
    return BOT_STATE
