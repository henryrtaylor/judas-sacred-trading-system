from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from signals_router import router as signals_router
from shadow_router import router as shadow_router

app = FastAPI()
app.include_router(signals_router)
app.include_router(shadow_router)

html_content = '''
<!DOCTYPE html>
<html>
<head><title>Judas Enhanced Dashboard</title></head>
<body>
<h1>📊 Judas Live Dashboard</h1>
<p>Signals: <a href="/api/signals">/api/signals</a></p>
<p>Shadow Positions: <a href="/api/shadow">/api/shadow</a></p>
<p>Shadow Trades: <a href="/api/trades">/api/trades</a></p>
</body>
</html>
'''

@app.get("/", response_class=HTMLResponse)
async def root():
    return HTMLResponse(content=html_content)
