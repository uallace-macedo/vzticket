import logging
import zoneinfo
from datetime import datetime, timedelta, timezone
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from vzticket.core.database import AsyncSessionLocal
from vzticket.modules.events_payout.service import EventPayoutService

logger = logging.getLogger('uvicorn.error')

scheduler = AsyncIOScheduler()
LOCAL_TZ = zoneinfo.ZoneInfo("America/Sao_Paulo")


async def run_daily_payout_tasks():
    logger.info('[CRON] Iniciando rotina diária de repasses de eventos...')
    
    async with AsyncSessionLocal() as session:
        payout_service = EventPayoutService(session)
        
        try:
            scheduled = await payout_service.schedule_payouts_for_today_events()
            logger.info(f'[CRON] Eventos agendados para payout hoje: {scheduled}')

            processed = await payout_service.process_due_payouts()
            logger.info(f'[CRON] Eventos finalizados e pagos (D+1): {processed}')
            
        except Exception as e:
            logger.error(f'[CRON] Erro ao executar rotina de repasses: {str(e)}', exc_info=True)


def start_scheduler():
    trigger = CronTrigger(hour=0, minute=0, second=0, timezone=LOCAL_TZ)
    scheduler.add_job(
        run_daily_payout_tasks,
        trigger=trigger,
        id='daily_payout_job',
        replace_existing=True,
        misfire_grace_time=3600
    )
    
    scheduler.start()
    logger.info('[CRON] APScheduler iniciado com sucesso!')


def shutdown_scheduler():
    if scheduler.running:
        scheduler.shutdown()
        logger.info('[CRON] APScheduler desligado.')
