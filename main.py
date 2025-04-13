'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 2023/10/04
Ending 2024//

'''
# Installing the necessary libraries
import os
import logging
import csv
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import fake_useragent
import pandas as pd

# Configure logging
logging.basicConfig(
    filename='parser.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class WebDriverWrapper:
    """AI is creating summary for
    """
    def __init__(self):
        # Creating an instance of Chrome WebDriver with the path to the driver and options to disable the browser window
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        self.chrome_options.add_argument(f'--user-agent={fake_useragent.UserAgent().random}')
        self.driver = None

    def start_driver(self):
        """AI is creating summary for start_driver
        """
        self.driver = webdriver.Chrome(
            service=ChromeService(ChromeDriverManager().install()),
            options=self.chrome_options
        )

    def stop_driver(self):
        """AI is creating summary for stop_driver
        """
        if self.driver:
            self.driver.quit()


class DataProcessor:
    """AI is creating summary for

    Returns:
        [type]: [description]
    """
    @staticmethod
    def clean_data(file_path):
        """AI is creating summary for clean_data

        Args:
            file_path ([type]): [description]

        Returns:
            [type]: [description]
        """
        try:
            # Read CSV with pandas
            df = pd.read_csv(file_path, sep='^')
            # Replace non-standard minus with standard minus
            df = df.replace('−', '-', regex=True)
            # Remove rows with any empty values
            df_cleaned = df.dropna()
            # Save cleaned data back to the same file
            df_cleaned.to_csv(file_path, sep='^', index=False, encoding='utf-8')
            logging.info('Data cleaned successfully. Removed %d empty rows.', len(df) - len(df_cleaned))
            return True
        except Exception as e:
            logging.error("Error during data cleaning: %s", e)
            return False


class DataParser(WebDriverWrapper):
    """AI is creating summary for DataParser

    Args:
        WebDriverWrapper ([type]): [description]
    """
    def __init__(self):
        # Calling the constructor of the parent class
        super().__init__()
        self.data_processor = DataProcessor()

    def parse_and_save(self, selected_date):
        """AI is creating summary for parse_and_save

        Args:
            selected_date ([type]): [description]
        """
        try:
            self.start_driver()
            self.driver.get('https://mfd.ru/marketdata/?id=5&mode=0')
            time.sleep(5)
            # Finding an element with a table
            element = self.driver.find_element(By.XPATH, '//*[@id="marketDataList"]')
            table = element.find_element(By.XPATH, 'tbody[2]')
            # Create directory structure
            folder_name = selected_date.strftime("%Y-%m-%d")
            os.makedirs(f"data/{folder_name}", exist_ok=True)
            current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f'data/{folder_name}/mos_stock_{current_datetime}.csv'
            # Write raw data to CSV
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter='^')
                writer.writerow([
                    'Ticker', 'Time', 'Last Price', 'Change (abs)',
                    'Change (%)', 'Price before closing', 'Price at opening',
                    'Minimum price', 'Average overpriced', 'Pieces per day',
                    'Quantity per day', 'Rub', 'Number of transactions per day'
                ])
                rows = table.find_elements(By.TAG_NAME, 'tr')
                for row in rows:
                    # Get all the cells of the row
                    columns = row.find_elements(By.TAG_NAME, 'td')
                    # Extract the text from each cell and write it to a file
                    row_data = [column.text for column in columns]
                    writer.writerow(row_data)
            # Clean the data (remove empty rows)
            if os.path.exists(filename):
                self.data_processor.clean_data(filename)
            logging.info('The data is saved to a file: %s', filename)
            return filename
        except Exception as e:
            logging.error("Error during parsing: %s", e)
            return None
        finally:
            self.stop_driver()


def main():
    """AI is creating summary for main
    """
    data_parser = DataParser()
    while True:
        current_date = datetime.now().date()
        current_time = datetime.now().time()
    # Check if the hour is less than 19
        if current_date.weekday() < 5 and current_time.hour < 19:
            logging.info(f"Starting parsing for {current_date} %s")
            result_file = data_parser.parse_and_save(current_date)
            if result_file:
                logging.info("Parsing completed successfully. Data saved to %s", result_file)
            else:
                logging.warning("Parsing completed with errors")
        else:
            logging.error('The script will not be executed at the current time.')

        # Wait 10 minutes before next run
        time.sleep(600)


if __name__ == "__main__":
    main()
