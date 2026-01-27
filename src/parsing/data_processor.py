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
    @staticmethod
    def clean_data(data_list: list[dict]) -> list[dict] | bool:
        try:
            df = pd.DataFrame(data_list)

            # Convert update_time from string to datetime
            if 'update_time' in df.columns:
                df['update_time'] = pd.to_datetime(df['update_time'], errors='coerce')
            # Drop rows where key trading fields are all NaN or None
            key_fields = ['last_price', 'change', 'open_price', 'high', 'low']
            df = df.dropna(subset=key_fields, how='all')

            # Recalculate change_percent if column exists or contains NaN
            if 'change_percent' in df.columns:
                df['change_percent'] = np.where(
                    df['prev_price'].notna() & (df['prev_price'] != 0),
                    (df['change'] / df['prev_price']) * 100,
                    0
                )

            logging.info('Data cleaned successfully. Records remaining: %d', len(df))
            return df.to_dict(orient='records')

        except Exception as e:
            logging.error("Error during data cleaning: %s", e)
            return False
