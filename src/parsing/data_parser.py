import logging
import aiohttp
import pandas as pd
from src.parsing.data_processor import DataProcessor
from src.quotes.crud import insert_quote


MOEX_API_BASE = "https://iss.moex.com/iss"
ALL_TQBR_URL = f"{MOEX_API_BASE}/engines/stock/markets/shares/boards/TQBR/securities.json"


# Wrapper for making requests to MOEX API
class MOEXApiWrapper:
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session
        self.base_url = MOEX_API_BASE

    async def fetch_data(self, url: str) -> dict | None:
        try:
            async with self.session.get(
                url,
                params={"iss.meta": "off"},
                timeout=aiohttp.ClientTimeout(total=5)
            ) as response:
                response.raise_for_status()
                return await response.json()

        except aiohttp.ClientError as e:
            logging.error("Request error: %s", e)
            return None

        except Exception as e:
            logging.error("Unexpected error during data fetch: %s", e)
            return None


# Parser for processing stock data from MOEX API
class StockDataParser:
    def __init__(self, api_wrapper: MOEXApiWrapper):
        self.api_wrapper = api_wrapper
        self.data_processor = DataProcessor()

    # Fetch stock data from MOEX API
    async def fetch_quotes(self):
        data = await self.api_wrapper.fetch_data(ALL_TQBR_URL)

        if not data:
            logging.error("No data received from MOEX API")
            return None

        securities = data.get('securities', {})
        marketdata = data.get('marketdata', {})

        if not securities.get('data') or not marketdata.get('data'):
            logging.error("Incomplete data from MOEX API")
            return None

        return data

    # Process stock data from MOEX API
    async def process_quotes(self, data):
        try:
            securities = data.get('securities', {})
            marketdata = data.get('marketdata', {})

            sec_df = pd.DataFrame(
                securities['data'],
                columns=securities['columns']
            )

            mkt_df = pd.DataFrame(
                marketdata['data'],
                columns=marketdata['columns']
            )

            merged_df = sec_df.merge(
                mkt_df,
                on='SECID',
                how='inner'
            )

            data_list = []

            for _, row in merged_df.iterrows():
                stock = {
                    'ticker': row['SECID'],
                    'name': row.get('SHORTNAME', 'N/A'),
                    'last_price': row.get('LAST', 0),
                    'prev_price': row.get('PREVPRICE', 0),
                    'change': row.get('CHANGE', 0),
                    'change_percent': row.get('CHANGEPERCENT', 0),
                    'open_price': row.get('OPEN', 0),
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

            return cleaned_data

        except Exception as e:
            logging.error("Error during quote processing: %s", e)
            return None

    # Insert cleaned data into the database
    async def save_quotes(self, cleaned_data):
        try:
            for data_dict in cleaned_data:
                await insert_quote(
                    update_time=data_dict['update_time'],
                    ticker=data_dict['ticker'],
                    name=data_dict['name'],
                    last_price=data_dict['last_price'],
                    prev_price=data_dict['prev_price'],
                    change=data_dict['change'],
                    change_percent=data_dict['change_percent'],
                    open_price=data_dict['open_price'],
                    high=data_dict['high'],
                    low=data_dict['low'],
                    volume=data_dict['volume'],
                    value=data_dict['value'],
                    lot_size=data_dict['lot_size'],
                )

            logging.info("Data successfully collected, cleaned, and saved to the database")

            return True

        except Exception as e:
            logging.error("Error during saving quotes: %s", e)
            return False

    # Fetch, process, and save TQBR stock data
    async def parse_and_save(self):
        try:
            data = await self.fetch_quotes()

            if not data:
                return None

            cleaned_data = await self.process_quotes(data)

            if not cleaned_data:
                return None

            return await self.save_quotes(cleaned_data)

        except Exception as e:
            logging.error("Error during parsing or saving data: %s", e)
            return None
