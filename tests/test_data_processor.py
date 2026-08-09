import pandas as pd

from src.parsing.data_processor import DataProcessor


def test_parse_update_time_converts_string_to_datetime():
    processor = DataProcessor()

    df = pd.DataFrame({
        "update_time": ["2025-05-08 10:30:00"]
    })

    result = processor.parse_update_time(df)

    assert pd.api.types.is_datetime64_any_dtype(
        result["update_time"]
    )


def test_parse_update_time_removes_invalid_dates():
    processor = DataProcessor()

    df = pd.DataFrame({
        "update_time": [
            "2025-05-08 10:30:00",
            "invalid-date"
        ]
    })

    result = processor.parse_update_time(df)

    assert len(result) == 1


def test_drop_empty_key_fields_removes_empty_rows():
    processor = DataProcessor()

    df = pd.DataFrame({
        "last_price": [100, None],
        "change": [5, None],
        "open_price": [95, None],
        "high": [110, None],
        "low": [90, None]
    })

    result = processor.drop_empty_key_fields(df)

    assert len(result) == 1


def test_recalc_change_percent_calculates_percentage():
    processor = DataProcessor()

    df = pd.DataFrame({
        "change": [10],
        "prev_price": [100],
        "change_percent": [0]
    })

    result = processor.recalc_change_percent(df)

    assert result["change_percent"].iloc[0] == 10


def test_recalc_change_percent_returns_zero_when_previous_price_is_zero():
    processor = DataProcessor()

    df = pd.DataFrame({
        "change": [10],
        "prev_price": [0],
        "change_percent": [0]
    })

    result = processor.recalc_change_percent(df)

    assert result["change_percent"].iloc[0] == 0


def test_clean_data_returns_cleaned_list():
    processor = DataProcessor()

    data = [
        {
            "update_time": "2025-05-08 10:30:00",
            "last_price": 100,
            "change": 5,
            "prev_price": 95,
            "change_percent": 0,
            "open_price": 95,
            "high": 105,
            "low": 90
        }
    ]

    result = processor.clean_data(data)

    assert isinstance(result, list)
    assert result[0]["last_price"] == 100


def test_clean_data_returns_false_with_invalid_input():
    processor = DataProcessor()

    result = processor.clean_data(None)

    assert result is False
