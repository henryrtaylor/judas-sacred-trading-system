
from fastapi import APIRouter
from typing import Dict

router = APIRouter()

@router.get("/api/shadow")
async def get_shadow_status():
    return {
        "balance": 50000,
        "cash": 15000,
        "margin_used": 10000,
        "timestamp": "2025-04-04T00:00:00"
    }
