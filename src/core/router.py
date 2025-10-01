'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 01/10/2025
Ending //

'''
# Installing the necessary libraries
import os
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()

# Templates
templates = Jinja2Templates(directory=os.path.join("src", "templates"))


# Home page route
@router.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# About page route
@router.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})
