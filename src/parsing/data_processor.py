'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 08/05/2025
Ending //

'''
# Installing the necessary libraries
import logging
import pandas as pd
import numpy as np


class DataProcessor:
    # Convert 'update_time' to datetime
    def parse_update_time(self, df: pd.DataFrame) -> pd.DataFrame:
        if 'update_time' in df.columns:
            # Convert update_time from string to datetime
            df['update_time'] = pd.to_datetime(df['update_time'], format="%Y-%m-%d %H:%M:%S", errors='coerce')
            # Normalize update_time to a datetime object
            df['update_time'] = df['update_time'].apply(lambda x: x.to_pydatetime() if pd.notna(x) else None)
        return df

    # Remove rows where all key trading fields are empty
    def drop_empty_key_fields(self, df: pd.DataFrame) -> pd.DataFrame:
        key_fields = ['last_price', 'change', 'open_price', 'high', 'low']
        return df.dropna(subset=key_fields, how='all')

    # Recalculate the 'change_percent' column
    def recalc_change_percent(self, df: pd.DataFrame) -> pd.DataFrame:
        if 'change_percent' in df.columns and 'prev_price' in df.columns:
            df['change_percent'] = np.where(
                df['prev_price'].notna() & (df['prev_price'] != 0),
                (df['change'] / df['prev_price']) * 100,
                0
            )
        return df

    # Cleans data: parse dates, drop empty key fields, recalc percentages
    def clean_data(self, data_list: list[dict]) -> list[dict] | bool:
        try:
            df = pd.DataFrame(data_list)
            df = self.parse_update_time(df)
            df = self.drop_empty_key_fields(df)
            df = self.recalc_change_percent(df)

            logging.info('Data cleaned successfully. Records remaining: %d', len(df))
            return df.to_dict(orient='records')

        except Exception as e:
            logging.error("Error during data cleaning: %s", e)
            return False
