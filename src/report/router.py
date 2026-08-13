from datetime import date
import os

from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

from src.quotes.crud import get_quotes

from src.report.csv_generator import generate_csv_report

from src.report.xlsx_generator import generate_xlsx_report


router = APIRouter()

# Templates
templates = Jinja2Templates(directory=os.path.join("src", "templates"))


# Report page route
@router.get("/create_report", response_class=HTMLResponse)
async def create_report(request: Request):
    return templates.TemplateResponse(
        name="create_report.html",
        context={},
        request=request
    )


# Download CSV report route
@router.post("/download_report")
async def download_report(
    start_date: str = Form(...),
    end_date: str = Form(...),
    file_name: str = Form(...)
):

    quotes = await get_quotes(
        start_date=date.fromisoformat(start_date),
        end_date=date.fromisoformat(end_date)
    )

    csv_file = generate_csv_report(
        quotes=quotes,
        return_buffer=True
    )

    return StreamingResponse(
        csv_file,
        media_type="text/csv",
        headers={
            "Content-Disposition":
            f"attachment; filename={file_name}.csv"
        }
    )


# Download XLSX report route
@router.post("/download_xlsx_report")
async def download_xlsx_report(
    start_date: str = Form(...),
    end_date: str = Form(...),
    file_name: str = Form(...)
):
    quotes = await get_quotes(
        start_date=date.fromisoformat(start_date),
        end_date=date.fromisoformat(end_date)
    )

    xlsx_file = generate_xlsx_report(
        quotes=quotes,
        return_buffer=True
    )

    return StreamingResponse(
        xlsx_file,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={
            "Content-Disposition":
            f"attachment; filename={file_name}.xlsx"
        }
    )
