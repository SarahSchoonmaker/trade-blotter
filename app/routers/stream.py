from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session
from app.services.portfolio import get_positions, get_pnl
from app.main import get_market
from app.schemas import StreamPayload
import asyncio

router = APIRouter(prefix="/ws", tags=["stream"])

@router.websocket("/stream")
async def stream(ws: WebSocket, session: AsyncSession = Depends(get_session)):
    await ws.accept()
    md = get_market()
    q = await md.subscribe()
    try:
        while True:
            # Wait for next price snapshot
            prices = await q.get()
            # Compute positions and P&L
            positions = await get_positions(session)
            pnl = await get_pnl(session, prices)
            payload = StreamPayload(prices=prices, positions=positions, pnl=pnl).model_dump()
            await ws.send_json(payload)
            await asyncio.sleep(0)  # yield
    except WebSocketDisconnect:
        return
