from fastapi import FastAPI, Depends
from .schemas import BetCreate, BetOut
from .crud import create_bet, get_bets
from .db import SessionLocal, Base, engine
from .service import refresh_bet_statuses
from sqlalchemy.ext.asyncio import AsyncSession
import aiohttp
from contextlib import asynccontextmanager
import asyncio


async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async def _check_bets():
        while True:
            await refresh_bet_statuses()
            await asyncio.sleep(5)

    asyncio.create_task(_check_bets())

    yield

app = FastAPI(lifespan=lifespan, title="Bet Maker")


@app.get("/events")
async def get_events():
    async with aiohttp.ClientSession() as session:
        async with session.get("http://line-provider:8000/events") as resp:
            return await resp.json()


@app.post("/bet", response_model=BetOut)
async def place_bet(bet: BetCreate, db: AsyncSession = Depends(get_db)):
    return await create_bet(db, bet)


@app.get("/bets", response_model=list[BetOut])
async def list_bets(db: AsyncSession = Depends(get_db)):
    return await get_bets(db)
