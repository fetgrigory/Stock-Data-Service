from io import BytesIO

from openpyxl import Workbook

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

DEFAULT_FILENAME = "stock_report.xlsx"


# Function for generating XLSX report from quotes
def generate_xlsx_report(quotes, return_buffer=False):
    if not quotes:
        return None

    workbook = Workbook(write_only=True)
    sheet = workbook.create_sheet()

    # Writing header
    sheet.append(CSV_HEADERS)

    # Writing rows
    for quote in quotes:
        sheet.append([quote.get(field, "") for field in CSV_HEADERS])

    if return_buffer:
        buffer = BytesIO()
        workbook.save(buffer)

        # Reset buffer pointer before returning
        buffer.seek(0)
        return buffer

    # Writing report to file
    workbook.save(DEFAULT_FILENAME)

    return DEFAULT_FILENAME
