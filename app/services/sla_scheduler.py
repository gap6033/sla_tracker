from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.models.sla_clock import SlaClock
from app.enums.sla_clock import SlaClockStatus
from app.db.session import SessionLocal  
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy import select
import logging
from app.services.sla_alert_producer import push_alert

logger = logging.getLogger(__name__)

def run_sla_check():
    now = datetime.now(timezone.utc)
    with SessionLocal() as db:

        running_clocks = db.execute(
            select(SlaClock).where(
                SlaClock.status == SlaClockStatus.running.value,
                SlaClock.end_time == None
            )
        ).scalars().all()

        for clock in running_clocks:
            start_time: datetime = clock.start_time
            elapsed =  (now - start_time).total_seconds()
            sla_seconds = clock.sla_target
            remaining = sla_seconds - elapsed
            remaining_pct = remaining / sla_seconds

            if elapsed >= sla_seconds:
                logger.warning(f"{clock.clock_type} clock {clock.ticket_id} exceeded SLA")
                clock.status = SlaClockStatus.breached.value
                db.commit()
                push_alert(clock.ticket_id, f"{clock.clock_type} SLA Breached")
            elif remaining_pct <= 0.15:
                logger.info(f"{clock.clock_type} clock  {clock.ticket_id} nearing breach")
                push_alert(clock.ticket_id, f"{clock.clock_type} nearing Breached")

       

def start_sla_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        run_sla_check,
        trigger=IntervalTrigger(minutes=1),
        id="sla_check",
        name="Check SLA Clocks for Breaches",
        replace_existing=True,
        max_instances=1,
        coalesce=True 
    )
    scheduler.start()
    logger.info("SLA scheduler started.")
