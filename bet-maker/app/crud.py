from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from . import models, schemas


async def create_bet(db: AsyncSession, bet: schemas.BetCreate):
    new_bet = models.Bet(event_id=bet.event_id, amount=bet.amount)
    db.add(new_bet)
    await db.commit()
    await db.refresh(new_bet)
    return new_bet


async def get_bets(db: AsyncSession):
    result = await db.execute(select(models.Bet))
    return result.scalars().all()


async def update_bet_status(db: AsyncSession, bet_id: int, new_status: models.BetStatus):
    await db.execute(update(models.Bet).where(models.Bet.id == bet_id).values(status=new_status))
    await db.commit()
