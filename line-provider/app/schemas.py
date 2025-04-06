import decimal
from typing import Optional
from pydantic import BaseModel
from .models import EventState


class Event(BaseModel):
    event_id: str
    coefficient: Optional[decimal.Decimal] = None
    deadline: Optional[int] = None  # UNIX timestamp
    state: Optional[EventState] = None
