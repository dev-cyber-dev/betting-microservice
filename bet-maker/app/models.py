from sqlalchemy import Column, String, Float, Enum, Integer
from sqlalchemy.orm import Mapped, mapped_column
from .db import Base
import enum


class BetStatus(str, enum.Enum):
    PENDING = "pending"
    WON = "won"
    LOST = "lost"


class Bet(Base):
    __tablename__ = "bets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    event_id: Mapped[str] = mapped_column(String, index=True)
    amount: Mapped[float] = mapped_column(Float)
    status: Mapped[BetStatus] = mapped_column(
        Enum(BetStatus), default=BetStatus.PENDING)
