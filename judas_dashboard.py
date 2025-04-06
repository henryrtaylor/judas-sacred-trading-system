from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return HTMLResponse(
        content="""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Judas Live Dashboard</title>
        </head>
        <body>
            <h1>📊 Welcome to Judas Live Dashboard</h1>
            <p>This will be the central hub for live market signals, shadow sessions, and trade insights.</p>
        </body>
        </html>
        """,
        status_code=200
    )