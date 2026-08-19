from io import BytesIO

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.cell import WriteOnlyCell

# Expected report fields order
REPORT_HEADERS = [
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

    # Header styles
    title_font = Font(name='Calibri', size=16, bold=True, color="1B4D3E")
    header_fill = PatternFill(start_color="1B4D3E", end_color="1B4D3E", fill_type="solid")
    header_font = Font(name='Calibri', size=11, bold=True, color="FFFFFF")
    header_align = Alignment(horizontal='center', vertical='center')

    # Report title
    title_cell = WriteOnlyCell(sheet, value="Stock Data Service")
    title_cell.font = title_font
    sheet.append([title_cell])

    # Report information
    sheet.append(["Инструменты для анализа фондового рынка"])
    sheet.append([])
    sheet.append(["Экспорт выполнил: grigory@example.com"])
    sheet.append(["Дата выгрузки: 29.06.2026 14:30 (MSK)"])
    sheet.append([])

    # Add styled table headers
    styled_headers = []
    for header in REPORT_HEADERS:
        cell = WriteOnlyCell(sheet, value=header)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_align
        styled_headers.append(cell)

    sheet.append(styled_headers)

    # Add report data
    for quote in quotes:
        sheet.append([quote.get(field, "") for field in REPORT_HEADERS])

    if return_buffer:
        buffer = BytesIO()
        workbook.save(buffer)

        # Reset buffer position
        buffer.seek(0)
        return buffer

    # Save report to file
    workbook.save(DEFAULT_FILENAME)

    return DEFAULT_FILENAME
