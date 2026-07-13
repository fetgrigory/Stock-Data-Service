import os
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

# Templates
templates = Jinja2Templates(directory=os.path.join("src", "templates"))


# Report page route
@router.get("/create_report", response_class=HTMLResponse)
def create_report(request: Request):
    return templates.TemplateResponse(
        name="create_report.html",
        context={},
        request=request
    )
