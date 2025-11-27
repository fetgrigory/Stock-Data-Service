'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 08/05/2025
Ending //

'''
# Installing the necessary libraries
import logging
from datetime import datetime
import pandas as pd


# Clean and convert a list of dictionaries containing stock data
class DataProcessor:
    """AI is creating summary for

    Returns:
        [type]: [description]
    """
    @staticmethod
    def clean_data(data_list: list[dict]) -> list[dict]:
        """AI is creating summary for clean_data

        Args:
            data_list (list[dict]): [description]

        Returns:
            list[dict]: [description]
        """
        try:
            # Convert to DataFrame
            df = pd.DataFrame(data_list)
            # Replace non-standard minus and remove spaces
            df = df.apply(lambda col: col.astype(str).str.replace('−', '-').str.replace(' ', '') if col.dtype == object else col)

            # Remove percentage signs
            df = df.replace('%', '', regex=True)

            # Remove rows with empty values
            df = df.dropna()

            # Remove rows with invalid time format
            if 'Time' in df.columns:
                def is_invalid_time_format(date_str):
                    try:
                        datetime.strptime(date_str, '%H:%M:%S')
                        return False
                    except ValueError:
                        return True
                df = df[~df['Time'].apply(lambda x: is_invalid_time_format(str(x)))]

            # Convert numeric fields
            numeric_fields_float = [
                'Last Price', 'Change (abs)', 'Change (%)', 'Price before closing',
                'Price at opening', 'Minimum price', 'Average overpriced', 'Rub'
            ]
            numeric_fields_int = ['Pieces per day', 'Quantity per day', 'Number of transactions per day']

            for field in numeric_fields_float:
                if field in df.columns:
                    df[field] = pd.to_numeric(df[field], errors='coerce')

            for field in numeric_fields_int:
                if field in df.columns:
                    df[field] = pd.to_numeric(df[field], errors='coerce', downcast='integer')

            df = df.dropna()
            logging.info('Data cleaned successfully. Records remaining: %d', len(df))
            return df.to_dict(orient='records')

        except Exception as e:
            logging.error("Error during data cleaning: %s", e)
            return False

    # Converts 'Time' string to full datetime using the selected date
    @staticmethod
    def process_trade_time(row: dict, selected_date: datetime.date) -> dict:
        """AI is creating summary for process_trade_time

        Args:
            row (dict): [description]
            selected_date (datetime.date): [description]

        Returns:
            dict: [description]
        """
        trade_time_str = row.get('Time')
        if trade_time_str:
            try:
                row['TradeDatetime'] = datetime.combine(
                    selected_date,
                    datetime.strptime(trade_time_str, '%H:%M:%S').time()
                )
            except ValueError:
                row['TradeDatetime'] = None
        return row
