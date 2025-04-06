import aiohttp
from .models import BetStatus
from .crud import update_bet_status
from .db import SessionLocal
from sqlalchemy import select
from .models import Bet

LINE_PROVIDER_URL = "http://line-provider:8000"


async def fetch_event(event_id: str):
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{LINE_PROVIDER_URL}/event/{event_id}") as resp:
            if resp.status == 200:
                return await resp.json()
            return None


async def refresh_bet_statuses():
    async with SessionLocal() as db:
        result = await db.execute(select(Bet))
        bets = result.scalars().all()

        for bet in bets:
            if bet.status != BetStatus.PENDING:
                continue

            event = await fetch_event(bet.event_id)
            if event is None:
                continue

            if event["state"] == "FINISHED_WIN":
                await update_bet_status(db, bet.id, BetStatus.WON)
            elif event["state"] == "FINISHED_LOSE":
                await update_bet_status(db, bet.id, BetStatus.LOST)
