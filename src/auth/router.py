'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 01/10/2025
Ending //

'''
# Installing the necessary libraries
import os
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from . import service

router = APIRouter()

# Templates
templates = Jinja2Templates(directory=os.path.join("src", "templates"))


# Login page route
@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


# Verifies user credentials and redirects to /admin on success, or returns login page with error
@router.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    if service.verify_user(username, password):
        token = service.create_access_token(username)
        response = RedirectResponse(url="/admin", status_code=302)
        response.set_cookie(service.config.JWT_ACCESS_COOKIE_NAME, token)
        return response
    return templates.TemplateResponse("login.html", {"request": request, "error": True})


# Signup page route
@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


# Creates a new user, or returns signup page with error if user already exists
@router.post("/signup", response_class=HTMLResponse)
async def signup(request: Request, username: str = Form(...), password: str = Form(...)):
    try:
        service.create_user(username, password)
        return RedirectResponse(url="/login", status_code=302)
    except Exception:
        return templates.TemplateResponse("signup.html", {"request": request, "error": True})


# Renders the protected test page; accessible only with a valid access token
@router.get("/admin", response_class=HTMLResponse, dependencies=[Depends(service.security.access_token_required)])
async def admin_page(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})
