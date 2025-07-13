from sqlalchemy.orm import Session
from app.models.status_history import TicketStatusHistory
from datetime import datetime

def create_ticket_status_history(
    db: Session,
    ticket_id: str,
    old_status: str,
    new_status: str,
    created_at: datetime,
    updated_at: datetime,
    escalation_level: str
):
    TicketStatusHistory()
    status_record = TicketStatusHistory(
        ticket_id=ticket_id,
        created_at=created_at,
        updated_at=updated_at,
        old_status=old_status,
        new_status=new_status,
        escalation_level=escalation_level
    )
    db.add(status_record)
    db.flush()
    return status_record


def get_last_ticket_status_history(db: Session, ticket_id: str) -> TicketStatusHistory | None:
    return (
        db.query(TicketStatusHistory)
        .filter(TicketStatusHistory.ticket_id == ticket_id)
        .order_by(TicketStatusHistory.updated_at.desc())
        .first()
    )
