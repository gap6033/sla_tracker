from sqlalchemy import Column, Integer, String, ForeignKey, Enum as SqlEnum
from app.db.base import Base
from app.enums.sla_clock import SlaClockType, SlaClockStatus
from sqlalchemy.dialects.postgresql import TIMESTAMP

class SlaClock(Base):
    __tablename__ = "sla_clocks"

    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(String, ForeignKey("tickets.id", ondelete="CASCADE"), nullable=False, index=True)
    clock_type = Column(SqlEnum(SlaClockType), nullable=False)
    start_time = Column(TIMESTAMP(timezone=True), nullable=False)
    end_time = Column(TIMESTAMP(timezone=True), nullable=True)
    status = Column(SqlEnum(SlaClockStatus), nullable=False)
    sla_target = Column(Integer, nullable=False)
    
  