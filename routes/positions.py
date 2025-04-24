
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_positions():
    return [{"symbol": "AAPL", "qty": 10, "side": "LONG"}, {"symbol": "TSLA", "qty": 5, "side": "SHORT"}]
