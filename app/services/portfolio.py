from typing import Dict, List, Tuple
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Trade, Side
from app.schemas import Position, PnL

async def get_positions(session: AsyncSession) -> List[Position]:
    # Aggregate using signed quantities and signed cost
    # net_qty = sum(qty_signed); gross_cost = sum(price * qty_signed); avg_cost = gross_cost / net_qty
    stmt = select(
        Trade.symbol,
        func.sum(func.case((Trade.side == Side.BUY, Trade.qty), else_=-Trade.qty)).label("net_qty"),
        func.sum(func.case((Trade.side == Side.BUY, Trade.qty * Trade.price), else_=-Trade.qty * Trade.price)).label("gross_cost"),
    ).group_by(Trade.symbol)

    rows = (await session.execute(stmt)).all()
    positions: List[Position] = []
    for symbol, net_qty, gross_cost in rows:
        net_qty = net_qty or 0.0
        gross_cost = gross_cost or 0.0
        avg_cost = (gross_cost / net_qty) if net_qty else 0.0
        positions.append(Position(symbol=symbol, net_qty=float(net_qty), avg_cost=float(avg_cost)))
    return positions

async def get_pnl(session: AsyncSession, marks: Dict[str, float]) -> List[PnL]:
    positions = await get_positions(session)
    pnl_list: List[PnL] = []
    for pos in positions:
        mark = float(marks.get(pos.symbol, pos.avg_cost))
        unreal = (mark - pos.avg_cost) * pos.net_qty
        pnl_list.append(PnL(symbol=pos.symbol, net_qty=pos.net_qty, avg_cost=pos.avg_cost, mark=mark, unrealized=float(unreal)))
    return pnl_list
