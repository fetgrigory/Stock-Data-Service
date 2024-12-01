# Web-Scraper-for-parsing-financial-data
![1](https://github.com/Fetkulingr/Web-Scraper-for-parsing-financial-data/assets/103204349/bf5fd339-07f5-4b10-9cee-d9588faae5ee)

This Python program scrapes stock market data from `[mfd.ru](https://mfd.ru/marketdata/?id=5&mode=0)` and saves it to a CSV file.  It leverages the Selenium library to interact with the website and the `csv` library to handle data output.  The program utilizes an object-oriented programming (OOP) approach with class inheritance.

**Main Functions:**

1. **`WebDriverWrapper` Class:** This class acts as a base class for managing the Selenium WebDriver.  Its primary responsibilities are:

    * **`start_driver()`:** Initializes the Chrome WebDriver in headless mode (meaning the browser window doesn't appear). This is crucial for automated scripting.
    * **`stop_driver()`:** Properly quits the WebDriver instance, releasing resources.

2. **`DataParser` Class:** This class inherits from `WebDriverWrapper` using single inheritance. It extends the functionality to specifically parse and save data from `mfd.ru`.  Its main function is:

    * **`parse_and_save(selected_date)`:** This method performs the core data scraping and saving logic:
        * Navigates to the specified URL on `mfd.ru`.
        * Locates the relevant table element using XPath.
        * Extracts data from each row and column of the table.
        * Writes the extracted data to a CSV file named using the current date and time.  The file uses `^` as a delimiter.
        * Includes error handling using a `try...except` block to catch potential exceptions during the scraping process.
        * Includes a `finally` block to ensure the WebDriver is closed even if errors occur.

3. **Main Execution Loop:** The main part of the script contains a `while True` loop that runs indefinitely.  It checks the current date and time:

    * If it's a weekday (Monday-Friday) and before 7 PM (`current_time.hour < 19`), it calls `data_parser.parse_and_save()` to scrape and save the data.
    * Otherwise, it prints a message indicating that the script won't execute at the current time.
    * The loop pauses for 10 minutes (`time.sleep(600)`) before repeating.


**OOP and Inheritance:**

The program demonstrates the principles of OOP through the use of classes and inheritance.  The `DataParser` class inherits from `WebDriverWrapper`. This is a form of *single inheritance* because `DataParser` inherits from only one parent class. This inheritance promotes code reusability and organization by separating concerns:  `WebDriverWrapper` handles the WebDriver management, while `DataParser` focuses on the specific tasks of data parsing and saving. This structure makes the code more modular, easier to maintain, and potentially easier to extend in the future.  For instance, you could create additional classes to handle data from different websites without modifying the core WebDriver management.

### Подготовка виртуального окружения и запуск программы

1. Создайте виртуальное окружение для изоляции зависимостей проекта. 
   Используйте команду:
   ```bash
   python -m venv venv
   ```

2. Активируйте виртуальное окружение:
   - На Windows:
     ```bash
     venv\Scripts\activate
     ```
   - На macOS и Linux:
     ```bash
     source venv/bin/activate
     ```
3. Запустите программа командой:
   ```bash
   python main.py
   ```
# Описание программы
Применяемые библиотеки:<br />
selenium               4.9.1 <br />
Cсылка на скачивание драйвера Chrome:https://googlechromelabs.github.io/chrome-for-testing/
