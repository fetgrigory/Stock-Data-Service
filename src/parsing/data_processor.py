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
    """
    # Converting a time string to a datetime object with the current date.
    @staticmethod
    def convert_time_to_timestamp(time_str: str) -> datetime:
        """AI is creating summary for convert_time_to_timestamp

        Args:
            time_str (str): [description]

        Returns:
            datetime: [description]
        """
        today = datetime.now().date()
        datetime_str = f"{today} {time_str}"
        try:
            return datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S")
        except ValueError as e:
            logging.error(f"Ошибка при преобразовании времени {time_str}: {e}")
            return None

    @staticmethod
    def clean_data(data_list: list[dict]) -> list[dict] | bool:
        try:
            # Convert a list of dictionaries to a DataFrame
            df = pd.DataFrame(data_list)

            # Replace non-standard minus with standard minus
            df = df.replace('−', '-', regex=True)

            # Remove spaces and percentages from all string columns
            str_cols = df.select_dtypes(include='object').columns
            df[str_cols] = df[str_cols].apply(
                lambda col: col.str.replace(' ', '').str.replace('%', '', regex=False)
            )

            # Function to check if the string matches the incorrect format 'dd.mm.yyyyHH:MM:SS'
            if 'Time' in df.columns:
                def is_invalid_time_format(date_str):
                    try:
                        pd.to_datetime(date_str, format='%d.%m.%Y%H:%M:%S', errors='raise')
                        return True
                    except Exception:
                        return False

                df = df[~df['Time'].apply(lambda x: is_invalid_time_format(str(x)))]
                # Convert numeric fields (float)
            numeric_fields_float = [
                'Last Price', 'Change (abs)', 'Change (%)', 'Price before closing',
                'Price at opening', 'Minimum price', 'Average overpriced', 'Rub'
            ]
            for field in numeric_fields_float:
                if field in df.columns:
                    df[field] = pd.to_numeric(
                        df[field].str.replace('+', '').str.replace(',', '.', regex=False),
                        errors='coerce'
                    )

            # Convert numeric fields (int)
            numeric_fields_int = [
                'Pieces per day', 'Quantity per day', 'Number of transactions per day'
            ]
            for field in numeric_fields_int:
                if field in df.columns:
                    df[field] = pd.to_numeric(
                        df[field].str.replace('+', '').str.replace(',', '').str.replace(' ', '', regex=False),
                        errors='coerce', downcast='integer')

            # Remove rows with any empty values
            df = df.dropna(how='any')

            logging.info('Data cleaned successfully. Records remaining: %d', len(df))
            return df.to_dict(orient='records')

        except Exception as e:
            logging.error("Error during data cleaning: %s", e)
            return False
