
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_status():
    return {"heartbeat": "alive", "timestamp": "2025-04-04T22:00:00"}
