from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from app.db import get_session
from app.models import Trade, Side
from app.schemas import TradeIn, TradeOut, Position, PnL
from app.services.portfolio import get_positions, get_pnl
from typing import List, Dict
from fastapi import Query
from app.main import get_market

router = APIRouter(prefix="", tags=["trading"])

@router.post("/trades", response_model=TradeOut)
async def create_trade(payload: TradeIn, session: AsyncSession = Depends(get_session)):
    # Basic validation: only BUY/SELL, positive qty/price handled by schema
    trade = Trade(symbol=payload.symbol.upper(), side=payload.side, qty=payload.qty, price=payload.price)
    session.add(trade)
    await session.commit()
    await session.refresh(trade)
    return trade

@router.get("/trades", response_model=List[TradeOut])
async def list_trades(limit: int = Query(100, le=1000), session: AsyncSession = Depends(get_session)):
    stmt = select(Trade).order_by(desc(Trade.ts)).limit(limit)
    rows = (await session.execute(stmt)).scalars().all()
    return rows

@router.get("/positions", response_model=List[Position])
async def positions(session: AsyncSession = Depends(get_session)):
    return await get_positions(session)

@router.get("/prices", response_model=Dict[str, float])
async def prices():
    md = get_market()
    return md.prices

@router.get("/pnl", response_model=List[PnL])
async def pnl(session: AsyncSession = Depends(get_session)):
    md = get_market()
    return await get_pnl(session, md.prices)
