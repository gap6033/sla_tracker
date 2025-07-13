from fastapi import FastAPI
from app.api.v1 import tickets
from app.api.v1 import health_check
from app.db.base import Base
from app.db.session import engine
from app.core.config import settings
from contextlib import asynccontextmanager
from app.core.sla_config import _load_yaml_config, _set_config, start_sla_config_watcher
from app.services.sla_alert_consumer import start_sla_alert_consumer
from app.services.sla_scheduler import start_sla_scheduler
import logging

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    _set_config(_load_yaml_config())
    start_sla_config_watcher()
    logger.info("SLA Config watcher started")
    start_sla_scheduler()
    logger.info("SLA Scheduler started")
    start_sla_alert_consumer()
    logger.info("SLA Consumer started")

    yield

Base.metadata.create_all(bind=engine)

app = FastAPI(lifespan=lifespan, title=settings.PROJECT_NAME, version=settings.VERSION)



app.include_router(tickets.router, prefix="/api/v1")
app.include_router(health_check.router, prefix="/api/v1")

