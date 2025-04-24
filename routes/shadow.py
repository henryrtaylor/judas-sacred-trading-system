
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_shadow_data():
    return {"shadow_balance": 50000, "equity": 62000, "drawdown": 3.5}
