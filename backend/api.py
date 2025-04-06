
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/status")
async def get_status():
    return {"status": "online", "message": "Judas backend is live."}

@app.get("/api/positions")
async def get_positions():
    return {
        "positions": [
            {"symbol": "AAPL", "qty": 10, "avg_price": 162.4},
            {"symbol": "TSLA", "qty": 5, "avg_price": 702.3}
        ]
    }

@app.get("/api/shadow")
async def get_shadow_data():
    return {
        "shadow_balance": 100000.0,
        "open_trades": [
            {"symbol": "NVDA", "side": "BUY", "qty": 2, "entry_price": 288.4}
        ]
    }
