'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 09/07/2025
Ending //

'''
# Installing the necessary libraries
import logging
import time
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

    def parse_and_save(self):
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
                # Create a dictionary from the table row and add it to the list
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

            # Clean data before saving
            cleaned_data = self.data_processor.clean_data(data_list)
            if not cleaned_data:
                logging.error("No valid data to insert after cleaning")
                return None

            # Insert cleaned data into the database
            for data_dict in cleaned_data:
                insert_quote(
                    ticker=data_dict['Ticker'],
                    trade_time=data_dict['Time'],
                    last_price=data_dict['Last Price'],
                    change_abs=data_dict['Change (abs)'],
                    change_percent=data_dict['Change (%)'],
                    price_before_closing=data_dict['Price before closing'],
                    price_at_opening=data_dict['Price at opening'],
                    minimum_price=data_dict['Minimum price'],
                    average_overpriced=data_dict['Average overpriced'],
                    pieces_per_day=data_dict['Pieces per day'],
                    quantity_per_day=data_dict['Quantity per day'],
                    rub=data_dict['Rub'],
                    num_transactions_per_day=data_dict['Number of transactions per day'],
                )

            logging.info("Data successfully collected, cleaned, and saved to the database")
            return True

        except Exception as e:
            logging.error("Error during parsing or saving data: %s", e)
            return None
        finally:
            self.stop_driver()
