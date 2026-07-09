import logging
import os
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from src.parsing.data_archiver import DataArchiver


os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename='logs/parser.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    encoding='utf-8'
)

logger = logging.getLogger(__name__)


class Scheduler:

    def __init__(self, parser, archiver=None, work_hours=None):
        self.parser = parser
        self.archiver = archiver or DataArchiver()
        self.work_hours = work_hours or {
            "start_time": "10:00",
            "end_time": "19:00",
            "work_days": [0, 1, 2, 3, 4],
        }

        self.scheduler = AsyncIOScheduler()

    def _within_work_hours(self):
        now = datetime.now()
        start = datetime.strptime(self.work_hours["start_time"], "%H:%M").time()
        end = datetime.strptime(self.work_hours["end_time"], "%H:%M").time()
        return now.weekday() in self.work_hours["work_days"] and start <= now.time() <= end

    # Parses data for the current date during business hours
    async def parse_job(self):
        if not self._within_work_hours():
            return
        now = datetime.now()
        logger.info("Starting parsing for %s", now.date())

        try:
            result = await self.parser.parse_and_save()

            if result:
                logger.info("Parsing completed successfully.")
            else:
                logger.warning("Parsing completed with errors.")

        except Exception as error:
            logger.exception("Parsing failed: %s", error)

    # Archiving task: performed at the end of the working day
    async def archive_job(self):
        now = datetime.now()
        end_time = datetime.strptime(
            self.work_hours["end_time"],
            "%H:%M"
        ).time()

        if now.weekday() in self.work_hours["work_days"] and now.time() >= end_time:

            logger.info("Starting archiving for %s", now.date())

            try:
                result = await self.archiver.archive(now.date())

                if result:
                    logger.info("Archiving completed successfully.")
                else:
                    logger.warning("Archiving failed or skipped.")

            except Exception as error:
                logger.exception("Archiving failed: %s", error)

    # Configures and starts asynchronous scheduler
    async def start_schedule(self):
        await self.parse_job()

        logger.info("Scheduler started.")

        # Scheduling parsing task every 10 minutes
        self.scheduler.add_job(
            self.parse_job,
            trigger="interval",
            minutes=10
        )

        end_time = self.work_hours["end_time"]

        hour, minute = map(int, end_time.split(":"))

        self.scheduler.add_job(
            self.archive_job,
            trigger="cron",
            hour=hour,
            minute=minute
        )

        self.scheduler.start()
