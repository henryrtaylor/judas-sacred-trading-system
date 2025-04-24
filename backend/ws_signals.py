from fastapi import APIRouter, WebSocket
import asyncio

router = APIRouter()

@router.websocket("/ws/signals")
async def websocket_signals(websocket: WebSocket):
    await websocket.accept()
    while True:
        await asyncio.sleep(2)
        await websocket.send_json({"symbol": "AAPL", "signal": "BUY"})