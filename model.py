from pydantic import BaseModel
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
    slug: str
    active: bool


class Event(BaseModel):
    name: str
    slug: str
    active: bool
    sport_id: Sport
    status: EventType
    scheduled_start: datetime
    actual_start: datetime


class Selection(BaseModel):
    name: str
    slug: str
    active: bool
    sport_id: Sport
    status: SelectionStatus
    scheduled_start: datetime
    actual_start: datetime
    price: float
    outcome: OutcomeType


