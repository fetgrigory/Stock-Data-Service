import csv
from datetime import datetime
from io import StringIO


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
    "lot_size"
]


def generate_csv_report(quotes, selected_date, return_bytes=False):
    if not quotes:
        print("No data available for report.")
        return None

        # Generate a unique filename using the current timestamp
    current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"mos_stock_{current_datetime}.csv"

    if return_bytes:
        output = StringIO()
        # Use '^' as a delimiter to avoid conflicts with decimal separators in financial data
        writer = csv.DictWriter(
            output,
            fieldnames=CSV_HEADERS,
            delimiter='^'
        )

        writer.writeheader()

        for row in quotes:
            writer.writerow(row)

        output.seek(0)
        return output

    else:
        with open(file_name, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(
                f,
                fieldnames=CSV_HEADERS,
                delimiter='^'
            )

            writer.writeheader()

            for row in quotes:
                writer.writerow(row)

        print(f"CSV report successfully generated at {file_name}")
        return file_name
