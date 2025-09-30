'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 04/10/2023
Ending //

'''
# Installing the necessary libraries
import time
import logging
from datetime import datetime
from src.parsing.data_parser import DataParser
from src.parsing.data_archiver import DataArchiver
from src.config import PARSER_SCHEDULE


def is_within_schedule():
    """AI is creating summary for is_within_schedule

    Returns:
        [type]: [description]
    """
    now = datetime.now()
    current_time = now.time()
    current_weekday = now.weekday()
    start_time = datetime.strptime(PARSER_SCHEDULE["start_time"], "%H:%M").time()
    end_time = datetime.strptime(PARSER_SCHEDULE["end_time"], "%H:%M").time()
    work_days = PARSER_SCHEDULE["work_days"]

    return (current_weekday in work_days and start_time <= current_time <= end_time)


def main():
    """AI is creating summary for main
    """
# Configure logging
    logging.basicConfig(
        filename='parser.log',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s')

    parser = DataParser()

    while True:
        current_datetime = datetime.now()
        current_date = current_datetime.date()
        current_time = current_datetime.time()
        if is_within_schedule():
            logging.info(f"Starting parsing for {current_date} %s")
            result_file = parser.parse_and_save(current_date)
            if result_file:
                logging.info("Parsing completed successfully. Data saved to %s", result_file)
            else:
                logging.warning("Parsing completed with errors")
        elif current_time >= datetime.strptime(PARSER_SCHEDULE["end_time"], "%H:%M").time():
            logging.info(f"Starting archiving for {current_date} %s")
            if DataArchiver.archive(current_date):
                logging.info("Archiving completed successfully.")
            else:
                logging.warning("Archiving failed or skipped.")
        else:
            logging.error('The script will not be executed at the current time.')

        # Wait 10 minutes before next run
        time.sleep(600)


if __name__ == "__main__":
    main()
