'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 09/07/2025
Ending //

'''
# Installing the necessary libraries
import logging
import requests
import pandas as pd
from src.parsing.data_processor import DataProcessor
from src.db.crud import insert_quote


MOEX_API_BASE = "https://iss.moex.com/iss"
ALL_TQBR_URL = f"{MOEX_API_BASE}/engines/stock/markets/shares/boards/TQBR/securities.json?iss.meta=off"


# Wrapper for making requests to MOEX API
class MOEXApiWrapper:
    """AI is creating summary for
    """
    def __init__(self):
        self.session = requests.Session()
        self.base_url = MOEX_API_BASE

    def fetch_data(self, url):
        """AI is creating summary for fetch_data

        Args:
            url ([type]): [description]

        Returns:
            [type]: [description]
        """
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logging.error("Request error: %s", e)
            return None
        except Exception as e:
            logging.error("Unexpected error during data fetch: %s", e)
            return None


# Parser for processing stock data from MOEX API
class StockDataParser(MOEXApiWrapper):
    """AI is creating summary for StockDataParser

    Args:
        MOEXApiWrapper ([type]): [description]
    """
    def __init__(self):
        super().__init__()
        self.data_processor = DataProcessor()
#Fetch, parse, clean, and save all TQBR stocks data
    def parse_and_save(self):
        try:
            data = self.fetch_data(ALL_TQBR_URL)
            if not data:
                logging.error("No data received from MOEX API")
                return None

            securities = data.get('securities', {})
            marketdata = data.get('marketdata', {})

            if not securities.get('data') or not marketdata.get('data'):
                logging.error("Incomplete data from MOEX API")
                return None

            sec_df = pd.DataFrame(securities['data'], columns=securities['columns'])
            mkt_df = pd.DataFrame(marketdata['data'], columns=marketdata['columns'])

            merged_df = sec_df.merge(mkt_df, on='SECID', how='inner')
            data_list = []

            for _, row in merged_df.iterrows():
                stock = {
                    'ticker': row['SECID'],
                    'name': row.get('SHORTNAME', 'N/A'),
                    'last_price': row.get('LAST', 0),
                    'prev_price': row.get('PREVPRICE', 0),
                    'change': row.get('CHANGE', 0),
                    'change_percent': row.get('CHANGEPERCENT', 0),
                    'open': row.get('OPEN', 0),
                    'high': row.get('HIGH', 0),
                    'low': row.get('LOW', 0),
                    'volume': row.get('VOLTODAY', 0),
                    'value': row.get('VALTODAY', 0),
                    'update_time': row.get('UPDATETIME', 'N/A'),
                    'lot_size': row.get('LOTSIZE', 1)
                }
                data_list.append(stock)

            # Clean data before saving
            cleaned_data = self.data_processor.clean_data(data_list)
            if not cleaned_data:
                logging.error("No valid data to insert after cleaning")
                return None

            # Insert cleaned data into the database
            for data_dict in cleaned_data:
                insert_quote(
                    ticker=data_dict['ticker'],
                    trade_time=data_dict['update_time'],
                    last_price=data_dict['last_price'],
                    change_abs=data_dict['change'],
                    change_percent=data_dict['change_percent'],
                    price_before_closing=data_dict['prev_price'],
                    price_at_opening=data_dict['open'],
                    minimum_price=data_dict['low'],
                    average_overpriced=data_dict['high'],
                    pieces_per_day=data_dict['volume'],
                    quantity_per_day=data_dict['value'],
                    rub=data_dict['value'],
                    num_transactions_per_day=data_dict['lot_size'],
                )

            logging.info("Data successfully collected, cleaned, and saved to the database")
            return True

        except Exception as e:
            logging.error("Error during parsing or saving data: %s", e)
            return None
