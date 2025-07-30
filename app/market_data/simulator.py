import asyncio
import random
from typing import Dict, List, Optional
from app.core.config import settings

class MarketData:
    def __init__(self, symbols: List[str], initial_prices: Optional[List[float]] = None):
        self.symbols = symbols
        if initial_prices and len(initial_prices) == len(symbols):
            self.prices: Dict[str, float] = {s: p for s, p in zip(symbols, initial_prices)}
        else:
            self.prices: Dict[str, float] = {s: random.uniform(50, 300) for s in symbols}
        self.subscribers: List[asyncio.Queue] = []

    async def subscribe(self) -> asyncio.Queue:
        q: asyncio.Queue = asyncio.Queue(maxsize=10)
        self.subscribers.append(q)
        # push the latest snapshot immediately
        await q.put(self.prices.copy())
        return q

    async def publish(self):
        for q in list(self.subscribers):
            try:
                if not q.full():
                    await q.put(self.prices.copy())
            except Exception:
                # drop broken queues
                try:
                    self.subscribers.remove(q)
                except ValueError:
                    pass

    async def run(self):
        tick = settings.tick_ms / 1000.0
        while True:
            # random walk per symbol
            for s in self.symbols:
                p = self.prices[s]
                # small drift + noise
                delta = random.gauss(0, p * 0.0005)
                self.prices[s] = max(0.01, p + delta)
            await self.publish()
            await asyncio.sleep(tick)
