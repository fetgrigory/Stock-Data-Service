'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 09/07/2025
Ending //

'''
# Installing the necessary libraries
import logging
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import fake_useragent
from src.parsing.data_processor import DataProcessor
from src.db.crud import insert_quote


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

    def parse_and_save(self, selected_date: datetime.date):
        """AI is creating summary for parse_and_save

        Args:
            selected_date (datetime.date): [description]

        Returns:
            [type]: [description]
        """
        try:
            self.start_driver()
            self.driver.get('https://mfd.ru/marketdata/?id=5&mode=0')
            time.sleep(5)
            # Finding an element with a table
            element = self.driver.find_element(By.XPATH, '//*[@id="marketDataList"]')
            table = element.find_element(By.XPATH, 'tbody[2]')
            data_list = []
            rows = table.find_elements(By.TAG_NAME, 'tr')
            # Get all the cells of the row
            for row in rows:
                columns = row.find_elements(By.TAG_NAME, 'td')
                row_data = [col.text for col in columns]
                if len(row_data) < 13:
                    continue

                data_dict = {
                    'Ticker': row_data[0],
                    'Time': row_data[1],
                    'Last Price': row_data[2],
                    'Change (abs)': row_data[3],
                    'Change (%)': row_data[4],
                    'Price before closing': row_data[5],
                    'Price at opening': row_data[6],
                    'Minimum price': row_data[7],
                    'Average overpriced': row_data[8],
                    'Pieces per day': row_data[9],
                    'Quantity per day': row_data[10],
                    'Rub': row_data[11],
                    'Number of transactions per day': row_data[12]
                }
                data_list.append(data_dict)

            cleaned_data_list = self.data_processor.clean_data(data_list)

            for row in cleaned_data_list:
                # Convert time to full datetime for DB
                trade_time_str = row['Time']
                trade_datetime = datetime.combine(
                    selected_date,
                    datetime.strptime(trade_time_str, '%H:%M:%S').time()
                )

                insert_quote(
                    ticker=row['Ticker'],
                    trade_time=trade_datetime,
                    last_price=row['Last Price'],
                    change_abs=row['Change (abs)'],
                    change_percent=row['Change (%)'],
                    price_before_closing=row['Price before closing'],
                    price_at_opening=row['Price at opening'],
                    minimum_price=row['Minimum price'],
                    average_overpriced=row['Average overpriced'],
                    pieces_per_day=row['Pieces per day'],
                    quantity_per_day=row['Quantity per day'],
                    rub=row['Rub'],
                    num_transactions_per_day=row['Number of transactions per day'],
                )

            return True

        except Exception as e:
            logging.error("Error during parsing: %s", e)
            return None
        finally:
            self.stop_driver()
