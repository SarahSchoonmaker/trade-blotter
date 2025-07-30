from pydantic import BaseModel, Field, ConfigDict
from typing import List, Dict
from datetime import datetime
from enum import Enum

class Side(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class TradeIn(BaseModel):
    symbol: str = Field(..., examples=["AAPL"])
    side: Side
    qty: float = Field(..., gt=0)
    price: float = Field(..., gt=0)

class TradeOut(BaseModel):
    id: int
    ts: datetime
    symbol: str
    side: Side
    qty: float
    price: float

    model_config = ConfigDict(from_attributes=True)

class Position(BaseModel):
    symbol: str
    net_qty: float
    avg_cost: float

class PnL(BaseModel):
    symbol: str
    net_qty: float
    avg_cost: float
    mark: float
    unrealized: float

class StreamPayload(BaseModel):
    prices: Dict[str, float]
    positions: List[Position]
    pnl: List[PnL]
