from enum import Enum

class TicketStatus(str, Enum):
    open = "open"
    responded = "responded"
    closed = "closed"
