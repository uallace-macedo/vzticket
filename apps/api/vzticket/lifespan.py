from contextlib import asynccontextmanager
from fastapi import FastAPI

from vzticket.core.cron import start_scheduler, shutdown_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield
    shutdown_scheduler()
