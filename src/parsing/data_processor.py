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

    # Unified time parser
    @staticmethod
    def parse_time(time_str: str):
        """AI is creating summary for parse_time

        Args:
            time_str (str): [description]

        Returns:
            [type]: [description]
        """
        try:
            return datetime.strptime(time_str, '%H:%M:%S').time()
        except (ValueError, TypeError):
            return None

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
            df = df.replace('−', '-', regex=True)
            # Remove spaces only inside string values
            str_cols = df.select_dtypes(include=['object']).columns
            df[str_cols] = df[str_cols].apply(lambda col: col.str.replace(' ', '', regex=False))
            # Remove percentage signs
            df = df.replace('%', '', regex=True)
            # Remove rows with empty values
            df = df.dropna()
            # Validate time field
            if 'Time' in df.columns:
                df['ParsedTime'] = df['Time'].apply(lambda x: DataProcessor.parse_time(str(x)))
                df = df[df['ParsedTime'].notna()]

            # Convert numeric fields (float)
            numeric_fields_float = [
                'Last Price', 'Change (abs)', 'Change (%)', 'Price before closing',
                'Price at opening', 'Minimum price', 'Average overpriced', 'Rub'
            ]

            for field in numeric_fields_float:
                if field in df.columns:
                    df[field] = pd.to_numeric(df[field], errors='coerce')

            # Convert numeric fields (int)
            numeric_fields_int = [
                'Pieces per day', 'Quantity per day', 'Number of transactions per day'
            ]
            for field in numeric_fields_int:
                if field in df.columns:
                    df[field] = pd.to_numeric(df[field], errors='coerce', downcast='integer')

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
        time_str = row.get('Time')
        parsed = DataProcessor.parse_time(time_str)
        row['TradeDatetime'] = (
            datetime.combine(selected_date, parsed) if parsed else None
        )
        return row
