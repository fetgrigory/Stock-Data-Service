import csv
from io import StringIO

# Expected report fields order
CSV_HEADERS = [
    "id",
    "update_time",
    "ticker",
    "name",
    "last_price",
    "prev_price",
    "change",
    "change_percent",
    "open",
    "high",
    "low",
    "volume",
    "value",
    "lot_size",
]

# Custom delimiter to avoid escaping issues
CSV_DELIMITER = "^"
DEFAULT_FILENAME = "stock_report.csv"


# Function for generating CSV report from quotes
def generate_csv_report(quotes, return_buffer=False):
    if not quotes:
        return None

    buffer = StringIO()
    # Creating CSV writer with custom headers and delimiter
    writer = csv.DictWriter(buffer, fieldnames=CSV_HEADERS, delimiter=CSV_DELIMITER)
    writer.writeheader()
    writer.writerows(quotes)

    if return_buffer:
        # Reset buffer pointer before returning
        buffer.seek(0)
        return buffer

    # Writing buffer content to file
    with open(DEFAULT_FILENAME, "w", newline="", encoding="utf-8") as file:
        file.write(buffer.getvalue())

    return DEFAULT_FILENAME
