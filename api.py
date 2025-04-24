from fastapi import FastAPI
from routers.strategy import strategy_router
from routers.shadow import shadow_router
from routers.status import status_router

app = FastAPI()

# Mount routers
app.include_router(strategy_router, prefix="/api/strategy")
app.include_router(shadow_router, prefix="/api/shadow")
app.include_router(status_router, prefix="/api/status")
