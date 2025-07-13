from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.models.sla_clock import SlaClock
from app.schemas.sla_clock import SlaClockCreate, SlaClockStatus, SlaClockType
from app.schemas.ticket import TicketIn


def start_clock(db: Session, sla_clock: SlaClockCreate) -> SlaClock:
    response_clock = SlaClock(**sla_clock.model_dump())
    db.add(response_clock)
    db.flush()
    return response_clock

def stop_clock(db: Session, clock: SlaClock, ticket: TicketIn):
    clock.status = SlaClockStatus.stopped
    clock.end_time = ticket.updated_at
    db.flush()
    return clock

def get_clock(db: Session, ticket_id: str, clock_type: SlaClockType) -> SlaClock | None:
    return db.query(SlaClock).filter(
        SlaClock.ticket_id == ticket_id,
        SlaClock.clock_type == clock_type
    ).first()
