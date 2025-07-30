from sqlalchemy import String, Integer, Float, DateTime, Enum as SAEnum
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime, timezone
from enum import Enum
from app.db import Base

class Side(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class Trade(Base):
    __tablename__ = "trades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ts: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    symbol: Mapped[str] = mapped_column(String(20), index=True, nullable=False)
    side: Mapped[Side] = mapped_column(SAEnum(Side), nullable=False)
    qty: Mapped[float] = mapped_column(Float, nullable=False)   # shares/contracts
    price: Mapped[float] = mapped_column(Float, nullable=False) # fill price
