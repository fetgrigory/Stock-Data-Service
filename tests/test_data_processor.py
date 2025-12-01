'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 05/08/2025
Ending //

'''
from src.parsing.data_processor import DataProcessor


# Tests for clean_string_for_numeric
def test_clean_string_for_numeric():
    """AI is creating summary for test_clean_string_for_numeric
    """
    # Checking the replacement of the minus
    assert DataProcessor.clean_string_for_numeric(" 100−5 ", is_float=True) == "100-5"
    # Check for deletion %
    assert DataProcessor.clean_string_for_numeric("50 %", is_float=True) == "50"
    # Check for removing spaces
    assert DataProcessor.clean_string_for_numeric(" 42 ", is_float=False) == "42"
