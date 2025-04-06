import time
from fastapi import FastAPI, Path, HTTPException
from .schemas import Event
from .models import EventState
import decimal

events: dict[str, Event] = {
    "1": Event(event_id="1", coefficient=decimal.Decimal("1.20"), deadline=int(time.time()) + 600, state=EventState.NEW),
    "2": Event(event_id="2", coefficient=decimal.Decimal("1.15"), deadline=int(time.time()) + 60, state=EventState.NEW),
    "3": Event(event_id="3", coefficient=decimal.Decimal("1.67"), deadline=int(time.time()) + 90, state=EventState.NEW),
}

app = FastAPI(title="Line Provider")


@app.get("/events")
async def get_events():
    """get all available events."""
    now = int(time.time())
    return [event for event in events.values() if event.deadline and event.deadline > now]


@app.get("/event/{event_id}")
async def get_event(event_id: str = Path(...)):
    """get event by id."""
    if event_id not in events:
        raise HTTPException(status_code=404, detail="Event not found")
    return events[event_id]


@app.put("/event")
async def create_or_update_event(event: Event):
    """create or update event."""
    if event.event_id not in events:
        events[event.event_id] = event
        return {"message": "Event created"}

    for key, value in event.dict(exclude_unset=True).items():
        setattr(events[event.event_id], key, value)

    return {"message": "Event updated"}
