
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from datetime import datetime

router = APIRouter()

class Signal(BaseModel):
    symbol: str
    signal: str
    confidence: float
    updated: datetime

@router.get("/api/signals", response_model=List[Signal])
async def get_mock_signals():
    return [
        {"symbol": "AAPL", "signal": "BUY", "confidence": 0.89, "updated": datetime.now()},
        {"symbol": "TSLA", "signal": "SELL", "confidence": 0.75, "updated": datetime.now()},
        {"symbol": "NVDA", "signal": "HOLD", "confidence": 0.5, "updated": datetime.now()}
    ]
