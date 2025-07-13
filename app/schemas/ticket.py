from pydantic import BaseModel, field_validator
from datetime import datetime, timezone
from app.enums.ticket import TicketStatus
from typing import List

class TicketIn(BaseModel):
    id: str
    priority: str
    updated_at: datetime
    created_at: datetime
    status: TicketStatus 
    customer_tier: str


    @field_validator("created_at", "updated_at", mode="before")
    @classmethod
    def normalize_to_utc(cls, v):
        # Parse string if needed
        if isinstance(v, str):
            v = datetime.fromisoformat(v)
        if not isinstance(v, datetime):
            raise ValueError("Invalid datetime format")

        return v.astimezone(timezone.utc) if v.tzinfo else v.replace(tzinfo=timezone.utc)
    
class TicketBatchIn(BaseModel):
    tickets: List[TicketIn]

    @field_validator('tickets')
    @classmethod
    def tickets_must_not_be_empty(cls, v):
        if not v:
            raise ValueError("At least one ticket must be provided")
        return v
    
    