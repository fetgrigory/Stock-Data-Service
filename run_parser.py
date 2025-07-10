'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 04/10/2023
Ending //

'''
# Installing the necessary libraries
import time
import logging
from datetime import datetime, time as dt_time
from data_parser import DataParser
from data_archiver import DataArchiver


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
        current_date = datetime.now().date()
        now = datetime.now()
        if parser.should_run():
            logging.info(f"Starting parsing for {current_date} %s")
            result_file = parser.parse_and_save(current_date)
            if result_file:
                logging.info("Parsing completed successfully. Data saved to %s", result_file)
            else:
                logging.warning("Parsing completed with errors")
        elif now.time() >= dt_time(19, 0):
            DataArchiver.archive(current_date)
        else:
            logging.error('The script will not be executed at the current time.')

        # Wait 10 minutes before next run
        time.sleep(600)


if __name__ == "__main__":
    main()
