def scan_markets():
    # Phase-A: dummy intelligent scan
    return [
        {
            "symbol": "NIFTY",
            "price": 120,
            "lot_size": 50,
            "sl_points": 20
        },
        {
            "symbol": "BANKNIFTY",
            "price": 180,
            "lot_size": 25,
            "sl_points": 30
        }
    ]

def detect_volatility():
    return "NORMAL"
