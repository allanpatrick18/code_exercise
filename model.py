from pydantic import BaseModel
from typing import Optional
from datetime import datetime, time, timedelta

from enum import Enum


class EventStatus(str, Enum):
    STARTED = "Started"
    ENDED = "Ended"
    PENDING = "Pending"
    CANCELLED = "Cancelled"


class EventType(str, Enum):
    PREPLAY = "Preplay"
    INPLAY = "Inplay"


class OutcomeType(str, Enum):
    WIN = "Win"
    VOID = "Void"
    LOSE = "Lose"
    UNSETTLED = 'Unsettled'


class Sports(BaseModel):
    id: Optional[int]
    name: str
    slug: Optional[str]
    active: bool


class Events(BaseModel):
    id: Optional[int]
    name: str
    slug: str
    type: EventType
    sport_id: int
    status: EventStatus
    active: bool
    scheduled_start: Optional[datetime]

    class Config:
        use_enum_values = True


class EventsIn(Events):
    actual_start: Optional[datetime]


class Selections(BaseModel):
    name: str
    slug: str
    active: bool
    event_id: int
    price: float
    outcome: OutcomeType

    class Config:
        use_enum_values = True


