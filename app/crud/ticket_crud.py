from sqlalchemy.orm import Session
from app.models.ticket import Ticket
from app.schemas.ticket import TicketIn
from sqlalchemy.exc import IntegrityError

def get_ticket(db: Session, id: str):
    return db.get(Ticket, id)

def create_ticket(db: Session, ticket_data: TicketIn) -> Ticket:
    ticket = Ticket(**ticket_data.model_dump())
    db.add(ticket)
    db.flush()
    return ticket
    

def update_ticket(db: Session, existing_ticket: Ticket, updated_ticket: TicketIn) -> Ticket:
    for field, value in updated_ticket.model_dump().items():
        setattr(existing_ticket, field, value)
    db.flush()
    return existing_ticket
        
