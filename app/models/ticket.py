from sqlalchemy import Column, String, Enum as SqlEnum, UniqueConstraint
from sqlalchemy.dialects.postgresql import TIMESTAMP
from app.db.base import Base
from app.enums.ticket import TicketStatus

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(String, primary_key=True)
    priority = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), nullable=False)
    status = Column(SqlEnum(TicketStatus), nullable=False)
    customer_tier = Column(String, nullable=False)
    escalation_level = Column(String, nullable=False, default="L1")

    __table_args__ = (
        UniqueConstraint("id", "updated_at", name="uix_ticket_id_updated_at"),
    )
