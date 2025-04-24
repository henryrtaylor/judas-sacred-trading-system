from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

@router.get("/api/account/shadow")
def get_shadow_status():
    return {
        "shadow_balance": 105432.12,
        "open_positions": [
            {"symbol": "TSLA", "qty": 10, "avg_price": 175.25}
        ],
        "last_trade": {
            "timestamp": str(datetime.now()),
            "symbol": "TSLA",
            "side": "BUY",
            "qty": 10,
            "price": 175.25
        }
    }