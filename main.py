'''
This module make

Athor: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 2023/10/04
Ending 2024//

'''
import csv
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# Path to the Chrome driver
chromedriver_path = 'C:\\Users\\Admin\\Desktop\\selenium_mos (от 12.10)\\chromedriver\\chromedriver.exe'
# Function to check if the date is a working day
def is_weekday(date):
    # Check if the day of the week is working (Monday-Friday)
    return date.weekday() < 5
# Function to check whether the time is before 19:00
def is_before_19_oclock(date):
    # Check if the hour is less than 19
    return date.hour < 19
# Function for parsing and saving data
def parse_and_save(selected_date):
    # Creating an instance of Chrome WebDriver with the path to the driver and options to disable the browser window
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    driver = webdriver.Chrome(service=Service(chromedriver_path), options=chrome_options)
    try:
    # Opening the data page
        driver.get(f'https://mfd.ru/marketdata/?id=5&mode=0')
        # Delay for data loading
        time.sleep(5)
        # Finding an element with a table
        element = driver.find_element(By.XPATH, '//*[@id="marketDataList"]')
        table = element.find_element(By.XPATH, 'tbody[2]')
       # Getting the current date and time for the file name
        current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # Generating a unique file name for each parsing
        filename = f'mos_stock_{selected_date}_{current_datetime}.csv'
       # Opening the file for recording
        with open(filename, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file, delimiter='^')
            # Writing column names to a file
            writer.writerow(['Ticker', 'Time', 'Transaction price_1', 'Transaction price_2', 'Transaction price_3', 'Price before closing', 'Price at opening', 'Minimum price', 'Average overpriced', 'Pieces per day', 'Quantity per day', 'Rub', 'Number of transactions per day'])
            # Getting all the rows of the table
            rows = table.find_elements(By.TAG_NAME, 'tr')
            # Write each line to a file
            for row in rows:
                # Get all the cells of the row
                columns = row.find_elements(By.TAG_NAME, 'td')
                # Extract the text from each cell and write it to a file
                row_data = [column.text for column in columns]
                writer.writerow(row_data)
            print(f'The data is saved to a file: {filename}')
    finally:
        # Closing the browser after parsing is completed
        driver.quit()
while True:
    # Get the current date and time
    current_date = datetime.now().date()
    current_time = datetime.now().time()
    # Check if the current date is a working day and the time is before 19:00
    if is_weekday(current_date) and is_before_19_oclock(current_time):
       # Start parsing and saving data
        parse_and_save(current_date)
    else:
        print('The script will not be executed at the current time.')
    time.sleep(600)
