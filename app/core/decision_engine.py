from datetime import datetime
from core.bot_state import BOT_STATE
from core.market_scanner import scan_markets, detect_volatility
from core.trade_risk_check import can_take_trade
from services.paper_executor import place_paper_trade

def run_autobot_cycle():
    BOT_STATE["status"] = "SCANNING"
    volatility = detect_volatility()
    opportunities = scan_markets()

    for opp in opportunities:
        ok, reason = can_take_trade(
            capital=BOT_STATE["capital"],
            used_exposure=BOT_STATE["used_exposure"],
            option_price=opp["price"],
            lot_size=opp["lot_size"],
            sl_points=opp["sl_points"],
            volatility=volatility,
            drawdown=BOT_STATE["drawdown"]
        )

        if not ok:
            continue

        trade_cost = opp["price"] * opp["lot_size"]
        BOT_STATE["used_exposure"] += trade_cost
        BOT_STATE["open_trades"] += 1

        place_paper_trade(opp)

    BOT_STATE["status"] = "TRADING"
    BOT_STATE["last_cycle"] = datetime.utcnow()
