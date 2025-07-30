import aiohttp
import asyncio
import logging
from typing import Dict, List
from app.core.config import settings

ALPHA_URL = "https://www.alphavantage.co/query"

class AlphaVantageMarketData:
    def __init__(self, symbols: List[str], api_key: str):
        self.symbols = symbols
        self.api_key = api_key
        self.prices: Dict[str, float] = {s: 0.0 for s in symbols}
        self.subscribers: List[asyncio.Queue] = []

    async def subscribe(self) -> asyncio.Queue:
        q: asyncio.Queue = asyncio.Queue(maxsize=10)
        self.subscribers.append(q)
        await q.put(self.prices.copy())
        return q

    async def publish(self):
        for q in list(self.subscribers):
            if not q.full():
                await q.put(self.prices.copy())

    async def fetch_price(self, session: aiohttp.ClientSession, symbol: str):
        try:
            params = {
                "function": "GLOBAL_QUOTE",
                "symbol": symbol,
                "apikey": self.api_key
            }
            async with session.get(ALPHA_URL, params=params) as resp:
                data = await resp.json()
                price = float(data["Global Quote"]["05. price"])
                self.prices[symbol] = price
        except Exception as e:
            logging.error(f"Failed to fetch price for {symbol}: {e}")

    async def run(self):
        interval = settings.tick_ms / 1000.0
        async with aiohttp.ClientSession() as session:
            while True:
                tasks = [self.fetch_price(session, s) for s in self.symbols]
                await asyncio.gather(*tasks)
                await self.publish()
                await asyncio.sleep(interval)
