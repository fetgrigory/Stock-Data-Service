'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 17/10/2025
Ending //
'''
# Installing the necessary libraries
import logging
import time
from datetime import datetime
import schedule
from src.parsing.data_archiver import DataArchiver
from src.parsing.data_parser import DataParser

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

logger = logging.getLogger(__name__)


class Scheduler:
    """AI is creating summary for
    """
    def __init__(self, parser=None, archiver=None, work_hours=None):
        self.parser = parser or DataParser()
        self.archiver = archiver or DataArchiver()
        self.work_hours = work_hours or {
            "start_time": "10:00",
            "end_time": "19:00",
            "work_days": [0, 1, 2, 3, 4],
        }

    def _within_work_hours(self):
        """AI is creating summary for _within_work_hours

        Returns:
            [type]: [description]
        """
        now = datetime.now()
        start = datetime.strptime(self.work_hours["start_time"], "%H:%M").time()
        end = datetime.strptime(self.work_hours["end_time"], "%H:%M").time()
        return now.weekday() in self.work_hours["work_days"] and start <= now.time() <= end

# Parses data for the current date during business hours
    def parse_job(self):
        """AI is creating summary for parse_job
        """
        if not self._within_work_hours():
            return
        now = datetime.now()
        logging.info("Starting parsing for %s", now.date())
        result_file = self.parser.parse_and_save(now.date())
        if result_file:
            logging.info("Parsing completed successfully. Data saved to %s", result_file)
        else:
            logging.warning("Parsing completed with errors.")

# Archiving task: performed at the end of the working day
    def archive_job(self):
        """AI is creating summary for archive_job
        """
        now = datetime.now()
        if now.weekday() in self.work_hours["work_days"] and now.time() >= datetime.strptime(self.work_hours["end_time"], "%H:%M").time():
            logging.info("Starting archiving for %s", now.date())
            if self.archiver.archive(now.date()):
                logging.info("Archiving completed successfully.")
            else:
                logging.warning("Archiving failed or skipped.")

# Configures and starts a schedule of parsing and archiving tasks
    def start_schedule(self):
        """AI is creating summary for start_schedule
        """
        # Scheduling tasks every 10 minutes
        self.parse_job()
        logging.info("Scheduler started.")
        schedule.every(10).minutes.do(self.parse_job)
        while True:
            schedule.run_pending()
            time.sleep(1)
