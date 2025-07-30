import asyncio
from fastapi import FastAPI
from sqlalchemy import text
from app.db import engine, Base
from app.core.config import settings
from app.market_data.simulator import MarketData
from app.routers.trades import router as trades_router
from app.routers.stream import router as stream_router
from app.market_data.alpha_vantage import AlphaVantageMarketData

app = FastAPI(title="Trading Blotter API")

# Global market data instance
_market: MarketData | None = None

def get_market() -> MarketData:
    assert _market is not None, "Market data not initialized"
    return _market

@app.on_event("startup")
async def on_startup():
    global _market
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    syms = [s.strip().upper() for s in settings.symbols]
    _market = AlphaVantageMarketData(syms, settings.alpha_vantage_key)
    asyncio.create_task(_market.run())

@app.get("/health")
async def health():
    return {"status": "ok"}

# Routers
app.include_router(trades_router)
app.include_router(stream_router)
