from datetime import datetime
import os
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from src.db.crud import get_quotes
from src.report.service import generate_csv_report

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


# Download report route
@router.get("/download_report")
async def download_report():
    quotes = await get_quotes()

    csv_file = generate_csv_report(
        quotes=quotes,
        selected_date=datetime.now(),
        return_bytes=True
    )

    return StreamingResponse(
        csv_file,
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=mos_stock_report.csv"
        }
    )
