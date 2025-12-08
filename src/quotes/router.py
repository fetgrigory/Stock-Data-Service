'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 06/12/2025
Ending //

'''
# Installing the necessary libraries
from pathlib import Path as SysPath
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from src.db.crud import get_all_quotes

router = APIRouter(tags=["Котировки 📈"])

# The absolute path to the templates folder
BASE_DIR = SysPath(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


# Endpoint for get quotes form
@router.get("/quotes")
def get_quotes_form(request: Request):
    # List of current quotes
    quotes = get_all_quotes()
    return templates.TemplateResponse("user.html", {"request": request, "quotes": quotes})