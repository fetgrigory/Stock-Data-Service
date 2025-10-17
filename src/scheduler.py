'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 17/10/2025
Ending //
'''
import logging
import time
from datetime import datetime
import schedule
from src.parsing.data_archiver import DataArchiver
from src.parsing.data_parser import DataParser

# Setting up working hours and days
WORK_HOURS = {
    "start_time": "10:00",
    "end_time": "19:00",
    "work_days": [0, 1, 2, 3, 4],
}

# Initializing the parser
parser = DataParser()


# Parses data for the current date during business hours
def parse_job():
    """AI is creating summary for parse_job
    """
    now = datetime.now()
    weekday = now.weekday()
    current_time = now.time()

    start_time = datetime.strptime(WORK_HOURS["start_time"], "%H:%M").time()
    end_time = datetime.strptime(WORK_HOURS["end_time"], "%H:%M").time()

    if weekday in WORK_HOURS["work_days"] and start_time <= current_time <= end_time:
        logging.info("Starting parsing for %s", now.date())
        result_file = parser.parse_and_save(now.date())
        if result_file:
            logging.info("Parsing completed successfully. Data saved to %s", result_file)
        else:
            logging.warning("Parsing completed with errors.")


# Archiving task: performed at the end of the working day
def archive_job():
    """AI is creating summary for archive_job
    """
    now = datetime.now()
    weekday = now.weekday()
    current_time = now.time()
    end_time = datetime.strptime(WORK_HOURS["end_time"], "%H:%M").time()

    # Archiving only on weekdays after business hours
    if weekday in WORK_HOURS["work_days"] and current_time >= end_time:
        logging.info("Starting archiving for %s", now.date())
        if DataArchiver.archive(now.date()):
            logging.info("Archiving completed successfully.")
        else:
            logging.warning("Archiving failed or skipped.")


# Configures and starts a schedule of parsing and archiving tasks
def start_schedule():
    """AI is creating summary for start_schedule
    """
    logging.basicConfig(
        filename='parser.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Task planning
    parse_job()
    logging.info("Scheduler started.")
    while True:
        schedule.run_pending()
        time.sleep(1)
