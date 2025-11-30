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


class DataProcessor:
    """AI is creating summary for

    Returns:
        [type]: [description]
    """
    # Clean a string to prepare for numeric conversion
    @staticmethod
    def clean_string_for_numeric(s: str, is_float: bool = True) -> str:
        """AI is creating summary for clean_string_for_numeric

        Args:
            s (str): [description]
            is_float (bool, optional): [description]. Defaults to True.

        Returns:
            str: [description]
        """
        if not isinstance(s, str):
            return s
        s = s.replace('−', '-')
        s = s.replace(' ', '')
        s = s.replace('+', '')
        if is_float:
            s = s.replace(',', '.')
            s = s.replace('%', '')
        else:
            s = s.replace(',', '')
        return s

    # Convert specified columns to numeric type
    @staticmethod
    def convert_numeric_columns(df: pd.DataFrame, columns: list[str], is_float: bool = True):
        """AI is creating summary for convert_numeric_columns

        Args:
            df (pd.DataFrame): [description]
            columns (list[str]): [description]
            is_float (bool, optional): [description]. Defaults to True.
        """
        for col in columns:
            if col in df.columns:
                df[col] = pd.to_numeric(
                    df[col].apply(lambda x: DataProcessor.clean_string_for_numeric(str(x), is_float)),
                    errors='coerce',
                    downcast=None if is_float else 'integer'
                )

    # Remove rows with incorrectly formatted time strings
    @staticmethod
    def filter_invalid_time(df: pd.DataFrame, column: str = 'Time') -> pd.DataFrame:
        """AI is creating summary for filter_invalid_time

        Args:
            df (pd.DataFrame): [description]
            column (str, optional): [description]. Defaults to 'Time'.

        Returns:
            pd.DataFrame: [description]
        """
        if column not in df.columns:
            return df

        def is_invalid_time_format(date_str):
            try:
                pd.to_datetime(date_str, format='%d.%m.%Y%H:%M:%S', errors='raise')
                return True
            except Exception:
                return False

        return df[~df[column].apply(lambda x: is_invalid_time_format(str(x)))]

    # Create a full datetime string by combining current date with time string
    @staticmethod
    def create_datetime_from_time(time_str: str) -> str:
        """AI is creating summary for create_datetime_from_time

        Args:
            time_str (str): [description]

        Returns:
            str: [description]
        """
        today = datetime.now().date()
        datetime_str = f"{today} {time_str}"
        return datetime_str

    # Clean and convert a list of dictionaries to a standardized format
    @staticmethod
    def clean_data(data_list: list[dict]) -> list[dict] | bool:
        """AI is creating summary for clean_data

        Returns:
            [type]: [description]
        """
        try:
            df = pd.DataFrame(data_list)

            # Standardize string columns
            str_cols = df.select_dtypes(include='object').columns
            df[str_cols] = df[str_cols].apply(lambda col: col.str.replace('−', '-').str.strip())

            # Remove invalid time formats
            df = DataProcessor.filter_invalid_time(df, 'Time')

            # Convert float columns
            float_columns = [
                'Last Price', 'Change (abs)', 'Change (%)', 'Price before closing',
                'Price at opening', 'Minimum price', 'Average overpriced', 'Rub'
            ]
            DataProcessor.convert_numeric_columns(df, float_columns, is_float=True)

            # Convert integer columns
            int_columns = ['Pieces per day', 'Quantity per day', 'Number of transactions per day']
            DataProcessor.convert_numeric_columns(df, int_columns, is_float=False)

            # Drop rows with any missing values
            df = df.dropna(how='any')

            logging.info('Data cleaned successfully. Records remaining: %d', len(df))
            return df.to_dict(orient='records')

        except Exception as e:
            logging.error("Error during data cleaning: %s", e)
            return False
