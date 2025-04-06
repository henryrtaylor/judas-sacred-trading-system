from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import random

router = APIRouter()

class Signal(BaseModel):
    symbol: str
    consensus: str
    confidence: float

@router.get("/api/signals", response_model=List[Signal])
def get_signals():
    symbols = ["AAPL", "TSLA", "NVDA", "AMD"]
    sentiments = ["BUY", "SELL", "NEUTRAL"]
    return [
        Signal(symbol=s, consensus=random.choice(sentiments), confidence=round(random.uniform(0.4, 0.9), 2))
        for s in symbols
    ]
