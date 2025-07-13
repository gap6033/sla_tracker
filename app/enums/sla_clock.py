from enum import Enum

class SlaClockType(str, Enum):
    response = "response"
    resolution = "resolution"

class SlaClockStatus(str, Enum):
    running = "running"
    stopped = "stopped"
    breached = "breached"
