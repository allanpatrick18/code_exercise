from pydantic import BaseModel
from typing import Optional
from datetime import datetime, time, timedelta

from enum import Enum



class SelectionStatus(str, Enum):
    STARTED = "Started"
    ENDED = "Ended"


class EventType(str, Enum):
    PREPLAY = "Preplay"
    INPLAY = "Inplay"


class OutcomeType(str, Enum):
    WIN = "Win"
    VOID = "Void"
    LOSE = "Lose"


class Sport(BaseModel):
    name: str
    slug: Optional[str]
    active: bool


class Event(BaseModel):
    name: str
    slug: str
    active: bool
    sport_id: int
    status: EventType

    class Config:
        use_enum_values = True


class EventIn(Event):
    scheduled_start: Optional[datetime]
    actual_start: Optional[datetime]


class Selection(BaseModel):
    name: str
    slug: str
    active: bool
    event_id: int
    status: SelectionStatus
    price: float
    outcome: OutcomeType

    class Config:
        use_enum_values = True


