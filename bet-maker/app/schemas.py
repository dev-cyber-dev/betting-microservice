from pydantic import BaseModel, Field
from enum import Enum


class BetStatus(str, Enum):
    pending = "pending"
    won = "won"
    lost = "lost"


class BetCreate(BaseModel):
    event_id: str
    amount: float = Field(..., gt=0)


class BetOut(BaseModel):
    id: int
    event_id: str
    amount: float
    status: BetStatus

    class Config:
        orm_mode = True
