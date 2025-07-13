from pydantic import BaseModel, field_validator
from datetime import datetime, timezone
from app.enums.sla_clock import SlaClockStatus, SlaClockType
from typing import Optional

class SlaClockCreate(BaseModel):
    ticket_id: str
    clock_type: SlaClockType
    start_time: datetime
    status: SlaClockStatus
    sla_target: int

    @field_validator('start_time', mode='before')
    @classmethod
    def to_utc(cls, v: datetime) -> datetime:
        # If it's already timezone-aware, convert to UTC
        if v.tzinfo is not None:
            return v.astimezone(timezone.utc)
        # If it's naive, assume it's in UTC and add tzinfo
        return v.replace(tzinfo=timezone.utc)

