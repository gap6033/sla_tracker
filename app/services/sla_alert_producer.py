import json
from datetime import datetime, timezone
from app.infra.redis_client import redis_client

REDIS_QUEUE_NAME = "sla_alerts"

def push_alert(ticket_id: str, event: str):
    alert = {
        "ticket_id": ticket_id,
        "event": event,
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

    redis_client.lpush(REDIS_QUEUE_NAME, json.dumps(alert))
