import json
from app.infra.redis_client import redis_client
import threading
import logging

logger = logging.getLogger(__name__)

REDIS_QUEUE_NAME = "sla_alerts"

def send_slack_notification(ticket_id, message):
    # Replace this with your real Slack webhook or API call
    logger.info(f"[Slack Notification] Ticket {ticket_id}: {message}")

def process_alert(alert_data):
    ticket_id = alert_data.get("ticket_id")
    event = alert_data.get("event")
    send_slack_notification(ticket_id, event)

def consume_alerts():
    logger.info("Starting Slack alert consumer...")
    while True:
        _, alert_json = redis_client.brpop(REDIS_QUEUE_NAME)
        try:
            alert_data = json.loads(alert_json)
            process_alert(alert_data)
        except Exception as e:
            logger.exception(f"Error processing alert: {e}")


def start_sla_alert_consumer():
    thread = threading.Thread(target=consume_alerts, daemon=True)
    thread.start()