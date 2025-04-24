from fastapi import APIRouter
from typing import List
from pydantic import BaseModel
import datetime

router = APIRouter()

class ShadowPosition(BaseModel):
    symbol: str
    qty: int
    avg_price: float

class ShadowTrade(BaseModel):
    timestamp: str
    symbol: str
    side: str
    qty: int
    price: float

@router.get("/api/shadow", response_model=List[ShadowPosition])
def get_shadow_positions():
    return [
        ShadowPosition(symbol="AAPL", qty=10, avg_price=150.25),
        ShadowPosition(symbol="TSLA", qty=5, avg_price=650.0),
    ]

@router.get("/api/trades", response_model=List[ShadowTrade])
def get_shadow_trades():
    now = datetime.datetime.now().isoformat()
    return [
        ShadowTrade(timestamp=now, symbol="AAPL", side="BUY", qty=10, price=150.25),
        ShadowTrade(timestamp=now, symbol="TSLA", side="SELL", qty=5, price=655.0),
    ]
