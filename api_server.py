# api_server.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/api/signals")
def get_signals():
    try:
        with open("logs/mock_signals.json") as f:
            return json.load(f)
    except:
        return []

@app.get("/api/trades")
def get_trades():
    try:
        with open("logs/trade_journal.json") as f:
            return json.load(f)
    except:
        return []

@app.get("/api/account")
def get_account():
    try:
        with open("logs/account_snapshot.json") as f:
            return json.load(f)
    except:
        return {}

@app.get("/api/status")
def get_status():
    return {"status": "Judas API is live"}