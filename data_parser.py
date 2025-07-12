'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 09/07/2025
Ending //

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
from data_processor import DataProcessor


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
