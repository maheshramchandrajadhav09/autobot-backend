from datetime import datetime

BOT_STATE = {
    "status": "IDLE",              # IDLE / SCANNING / TRADING / PAUSED
    "capital": 100000.0,
    "used_exposure": 0.0,
    "open_trades": 0,
    "drawdown": 0.0,
    "pnl_today": 0.0,
    "last_cycle": None
}
