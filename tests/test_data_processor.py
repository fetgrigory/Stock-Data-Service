'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 05/08/2025
Ending //

'''
# Installing the necessary libraries
import pandas as pd
from src.parsing.data_processor import DataProcessor


def test_clean_data(tmp_path):
    """AI is creating summary for test_clean_data

    Args:
        tmp_path ([type]): [description]
    """
    # Create a test CSV
    test_data = """col1^col2^col3\n1 000^10%^−5\n2 000^20%^−10"""
    file_path = tmp_path / "test.csv"
    file_path.write_text(test_data, encoding='utf-8')

    # Run the cleanup and check that the function completed successfully (returned True)
    result = DataProcessor.clean_data(file_path)
    assert result is True
    # Check the result
    df = pd.read_csv(file_path, sep='^', dtype=str)
    # Check for removing spaces
    assert df["col1"].iloc[0] == "1000"
    # Check for deletion %
    assert df["col2"].iloc[0] == "10"
    # Checking the replacement of the minus
    assert df["col3"].iloc[0] == "-5"
