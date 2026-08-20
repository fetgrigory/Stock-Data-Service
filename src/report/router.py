from datetime import date
from pathlib import Path
from urllib.parse import quote

from fastapi import APIRouter, Request, Form, HTTPException, Depends
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates

from src.auth.service import get_current_user
from src.quotes.crud import get_quotes
from src.report.analytics import calculate_quote_analytics
from src.report.csv_generator import generate_csv_report
from src.report.xlsx_generator import generate_xlsx_report

router = APIRouter()

# Templates
BASE_DIR = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=BASE_DIR / "src" / "templates")


# Report page route
@router.get("/create_report", response_class=HTMLResponse)
async def create_report(
    request: Request,
    user=Depends(get_current_user)
):
    return templates.TemplateResponse(
        name="create_report.html",
        context={
            "user": user
        },
        request=request,
    )


# Form safe Content-Disposition with UTF-8 filename support
def _make_disposition(filename: str, extension: str) -> str:
    safe_name = f"{filename}.{extension}"
    encoded = quote(safe_name, safe="")
    return f'attachment; filename="{safe_name}"; filename*=UTF-8\'\'{encoded}'


# Download CSV report route
@router.post("/download_csv_report")
async def download_csv_report(
    start_date: date = Form(...),
    end_date: date = Form(...),
    file_name: str = Form(...),
):
    if start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="start_date не может быть позже end_date")

    quotes = await get_quotes(start_date=start_date, end_date=end_date)
    csv_buffer = generate_csv_report(
        quotes=quotes,
        return_buffer=True
    )

    return StreamingResponse(
        csv_buffer,
        media_type="text/csv",
        headers={"Content-Disposition": _make_disposition(file_name, "csv")},
    )


# Download XLSX report route
@router.post("/download_xlsx_report")
async def download_xlsx_report(
    start_date: date = Form(...),
    end_date: date = Form(...),
    file_name: str = Form(...),
    user=Depends(get_current_user)
):
    if start_date > end_date:
        raise HTTPException(
            status_code=400,
            detail="start_date не может быть позже end_date")

    quotes = await get_quotes(start_date=start_date, end_date=end_date)
    analytics_df = calculate_quote_analytics(quotes)
    xlsx_buffer = generate_xlsx_report(
        analytics_df=analytics_df,
        user_email=user.email,
        return_buffer=True
    )

    return StreamingResponse(
        xlsx_buffer,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": _make_disposition(file_name, "xlsx")},
    )
