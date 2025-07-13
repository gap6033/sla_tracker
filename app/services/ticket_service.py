from sqlalchemy.orm import Session
from app.crud.ticket_crud import create_ticket, get_ticket, update_ticket
from app.schemas.ticket import TicketBatchIn, TicketIn
from app.crud.status_history_crud import create_ticket_status_history, get_last_ticket_status_history
from app.crud.sla_clock_crud import start_clock, get_clock, stop_clock
from app.schemas.sla_clock import SlaClockCreate
from app.enums.sla_clock import SlaClockType, SlaClockStatus
from app.core.sla_config import get_sla_target
from app.models.ticket import Ticket
from app.enums.ticket import TicketStatus
import logging

logger = logging.getLogger(__name__)


def ingest_tickets(payload: TicketBatchIn, db: Session):
    failure = []
    success = []
    for ticket_in in payload.tickets:
        try:
            with db.begin():
                ticket: Ticket = get_ticket(db, ticket_in.id)
                
                if ticket:
                    _handle_existing_ticket(ticket, ticket_in, db)
                else:
                    _handle_new_ticket(ticket_in, db)
                success.append(ticket_in.id)
        except Exception as e:
            failure.append(ticket_in.id)
            logger.exception(f"Failed to process ticket: {ticket_in.id}")
    return success, failure
            
                

def _handle_existing_ticket(ticket: Ticket, ticket_in: TicketIn, db:Session):
    if ticket.updated_at == ticket_in.updated_at:
        return  
    updated_ticket = update_ticket(db, ticket, ticket_in)
    last_ticket_status_history = get_last_ticket_status_history(db, updated_ticket.id)
    create_ticket_status_history(
        db,
        ticket_id=updated_ticket.id,
        old_status=last_ticket_status_history.new_status,
        new_status=updated_ticket.status,
        created_at=updated_ticket.created_at,
        updated_at=updated_ticket.updated_at,
        escalation_level = updated_ticket.escalation_level
    )
    if updated_ticket.status != TicketStatus.open.value:
        response_clock = get_clock(db, updated_ticket.id, SlaClockType.response.value)
        if not response_clock.end_time:
            stop_clock(db, response_clock, updated_ticket)

    if updated_ticket.status == TicketStatus.closed.value:
        resolution_clock = get_clock(db, updated_ticket.id, SlaClockType.resolution.value)
        if not resolution_clock.end_time:
            stop_clock(db, resolution_clock, updated_ticket)

   

def _handle_new_ticket(ticket_in: TicketIn, db:Session):
    new_ticket: Ticket = create_ticket(db, ticket_in)
    create_ticket_status_history(
        db,
        ticket_id=new_ticket.id,
        old_status=None,
        new_status=new_ticket.status,
        created_at=ticket_in.created_at,
        updated_at=ticket_in.updated_at,
        escalation_level = new_ticket.escalation_level
    )
    response_sla_target = get_sla_target(new_ticket.customer_tier, SlaClockType.response.value)
    response_clock = SlaClockCreate(ticket_id=new_ticket.id, 
                        clock_type=SlaClockType.response.value,
                        start_time=new_ticket.created_at,
                        status=SlaClockStatus.running.value, 
                        sla_target=response_sla_target)
    start_clock(db, response_clock)


    response_sla_target = get_sla_target(new_ticket.customer_tier, SlaClockType.resolution.value)
    resolution_clock = SlaClockCreate(ticket_id=new_ticket.id, 
                        clock_type=SlaClockType.resolution.value,
                        start_time=new_ticket.created_at,
                        status=SlaClockStatus.running.value, 
                        sla_target=response_sla_target)
    start_clock(db, resolution_clock)
   