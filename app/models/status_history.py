from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SqlEnum
from app.db.base import Base
from sqlalchemy.dialects.postgresql import TIMESTAMP
from app.enums.ticket import TicketStatus

class TicketStatusHistory(Base):
    __tablename__ = "ticket_status_history"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String, ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False)
    old_status = Column(SqlEnum(TicketStatus), nullable=True)
    new_status = Column(SqlEnum(TicketStatus), nullable=False)
    escalation_level = Column(String, nullable=False)


