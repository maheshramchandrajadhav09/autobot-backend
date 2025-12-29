import asyncio

STATUS = {}
RESULTS = {}

async def start_mock_parse(upload_id: str):
    STATUS[upload_id] = "processing"

    # simulate parsing delay
    await asyncio.sleep(3)

    RESULTS[upload_id] = {
        "trades": [
            {
                "symbol": "BANKNIFTY",
                "type": "BUY",
                "qty": 25,
                "price": 120.5
            }
        ],
        "charges": {
            "brokerage": 40,
            "gst": 7.2,
            "total": 47.2
        }
    }

    STATUS[upload_id] = "done"

def get_status(upload_id: str):
    return STATUS.get(upload_id, "unknown")

def get_result(upload_id: str):
    return RESULTS.get(upload_id)

