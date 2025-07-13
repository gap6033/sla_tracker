from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.ticket import TicketBatchIn
from app.services.ticket_service import ingest_tickets
from app.db.session import get_db

router = APIRouter()

@router.post("/tickets", summary="Create tickets", tags=["Tickets"])
def fetch_tickets(payload: TicketBatchIn, db: Session = Depends(get_db)):
    success, failure = ingest_tickets(payload, db)
    return {"message": f"{len(payload.tickets)} tickets processed. Failed: {failure}, Success: {success}"}
