import asyncio
from typing import Dict, Any

# In-memory stores (for mock only)
STATUS: Dict[str, str] = {}
RESULTS: Dict[str, Any] = {}


async def start_mock_parse(upload_id: str) -> None:
    """
    Simulates OCR + parsing work.
    Runs asynchronously in background.
    """

    STATUS[upload_id] = "processing"

    # simulate heavy OCR / parsing delay
    await asyncio.sleep(3)

    # mock parsed result
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
            "brokerage": 40.0,
            "gst": 7.2,
            "total": 47.2
        }
    }

    STATUS[upload_id] = "done"


def get_status(upload_id: str) -> str:
    """
    Returns current parsing status
    """
    return STATUS.get(upload_id, "unknown")


def get_result(upload_id: str):
    """
    Returns parsed result if available
    """
    return RESULTS.get(upload_id)
