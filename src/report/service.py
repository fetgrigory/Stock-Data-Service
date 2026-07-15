import csv
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


def generate_csv_report(
    quotes,
    return_bytes=False
):

    if not quotes:
        return None

    if return_bytes:

        output = StringIO()

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

        file_name = "stock_report.csv"

        with open(
            file_name,
            "w",
            newline="",
            encoding="utf-8"
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=CSV_HEADERS,
                delimiter='^'
            )

            writer.writeheader()

            for row in quotes:
                writer.writerow(row)

        return file_name
