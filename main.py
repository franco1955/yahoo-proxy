from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx, os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

YAHOO = "https://query1.finance.yahoo.com/v8/finance/chart/{symbol}"
HEADERS = {"User-Agent": "Mozilla/5.0"}

@app.get("/quote")
async def quote(symbol: str = Query(...), interval: str = "1h", range: str = "1mo"):
    url = YAHOO.format(symbol=symbol)
    params = {"interval": interval, "range": range, "includePrePost": "false"}
    async with httpx.AsyncClient(timeout=15) as client:
        r = await client.get(url, params=params, headers=HEADERS)
        return r.json()

@app.get("/")
def root():
    return {"status": "ok", "service": "Yahoo Finance Proxy"}
