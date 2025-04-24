
from fastapi import APIRouter
from typing import List
from pydantic import BaseModel

router = APIRouter()

class Position(BaseModel):
    symbol: str
    qty: int
    side: str
    pnl: float

@router.get("/api/positions", response_model=List[Position])
async def get_positions():
    return [
        {"symbol": "AAPL", "qty": 10, "side": "LONG", "pnl": 128.4},
        {"symbol": "TSLA", "qty": 5, "side": "SHORT", "pnl": -47.2}
    ]
