import os
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

# Templates
templates = Jinja2Templates(directory=os.path.join("src", "templates"))


# Home page route
@router.get("/", response_class=HTMLResponse)
def homepage(request: Request):
    return templates.TemplateResponse(
        name="index.html",
        context={},
        request=request
    )


# About page route
@router.get("/about", response_class=HTMLResponse)
def about(request: Request):
    return templates.TemplateResponse(
        name="about.html",
        context={},
        request=request
    )
