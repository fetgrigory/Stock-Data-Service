'''
This module make

Athor: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 2023/10/04
Ending 2024//

'''
# Installing the necessary libraries
import csv
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Path to the Chrome driver
chromedriver_path = 'chromedriver/chromedriver.exe'


class WebDriverWrapper:
    """AI is creating summary for
    """
    def __init__(self, chromedriver_path):
        self.chromedriver_path = chromedriver_path
    # Creating an instance of Chrome WebDriver with the path to the driver and options to disable the browser window
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')
        self.driver = None

    def start_driver(self):
        """AI is creating summary for start_driver
        """
        self.driver = webdriver.Chrome(service=Service(self.chromedriver_path),
                                       options=self.chrome_options)

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
    def __init__(self, chromedriver_path):
        # Calling the constructor of the parent class
        super().__init__(chromedriver_path)

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
            current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f'mos_stock_{selected_date}_{current_datetime}.csv'
            # Opening the file for recording
            with open(filename, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file, delimiter='^')
                writer.writerow(['Ticker', 'Time', 'Last Price', 'Change (abs)', 'Change (%)', 'Price before closing', 'Price at opening', 'Minimum price', 'Average overpriced', 'Pieces per day', 'Quantity per day', 'Rub', 'Number of transactions per day'])
                rows = table.find_elements(By.TAG_NAME, 'tr')
                for row in rows:
                    # Get all the cells of the row
                    columns = row.find_elements(By.TAG_NAME, 'td')
                    # Extract the text from each cell and write it to a file
                    row_data = [column.text for column in columns]
                    writer.writerow(row_data)
                print(f'The data is saved to a file: {filename}')
        except Exception as e:
            print(f"Error during parsing: {e}")
        finally:
            self.stop_driver()


data_parser = DataParser(chromedriver_path)

while True:
    current_date = datetime.now().date()
    current_time = datetime.now().time()
    # Check if the hour is less than 19
    if current_date.weekday() < 5 and current_time.hour < 19:
        data_parser.parse_and_save(current_date)
    else:
        print('The script will not be executed at the current time.')
    time.sleep(600)
