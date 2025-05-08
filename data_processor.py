'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 08/05/2025
Ending //

'''
# Installing the necessary libraries
import logging
import pandas as pd


class DataProcessor:
    """AI is creating summary for

    Returns:
        [type]: [description]
    """
    @staticmethod
    def clean_data(file_path):
        """AI is creating summary for clean_data

        Args:
            file_path ([type]): [description]

        Returns:
            [type]: [description]
        """
        try:
            # Read CSV with pandas
            df = pd.read_csv(file_path, sep='^')
            # Replace non-standard minus with standard minus
            df = df.replace('−', '-', regex=True)
            # Remove spaces in numbers (e.g., "1 000" → "1000")
            df = df.map(lambda x: str(x).replace(' ', '') if isinstance(x, str) else x)
            # Remove rows with any empty values
            df_cleaned = df.dropna()
            # Save cleaned data back to the same file
            df_cleaned.to_csv(file_path, sep='^', index=False, encoding='utf-8')
            logging.info('Data cleaned successfully. Removed %d empty rows.', len(df) - len(df_cleaned))
            return True
        except Exception as e:
            logging.error("Error during data cleaning: %s", e)
            return False
