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


# login page route
@router.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# signup page route
@router.get("/signup", response_class=HTMLResponse)
async def signup(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})
