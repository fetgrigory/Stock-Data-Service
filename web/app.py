'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 25/07/2025
Ending //

'''
# Installing the necessary libraries
import os
from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware
from .database import Base, engine, get_db
from .models import User

app = FastAPI()

# Templates and statics
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Secret key for flash messages via sessions
app.add_middleware(SessionMiddleware, secret_key="secret_key")

# Creating tables
Base.metadata.create_all(bind=engine)


# Home page route
@app.get("/", response_class=HTMLResponse)
@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    """AI is creating summary for home

    Args:
        request (Request): [description]

    Returns:
        [type]: [description]
    """
    return templates.TemplateResponse("index.html", {"request": request})


# About page route
@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    """AI is creating summary for about

    Args:
        request (Request): [description]

    Returns:
        [type]: [description]
    """
    return templates.TemplateResponse("about.html", {"request": request})


# Signup page route
@app.get("/signup", response_class=HTMLResponse)
async def signup_form(request: Request):
    """AI is creating summary for signup_form

    Args:
        request (Request): [description]

    Returns:
        [type]: [description]
    """
    return templates.TemplateResponse("signup.html", {"request": request})


@app.post("/signup", response_class=HTMLResponse)
async def process_signup(request: Request,
                 username: str = Form(...),
                 password: str = Form(...),
                 confirm_password: str = Form(...),
                 db: Session = Depends(get_db)):
    """AI is creating summary for process_signup

    Args:
        request (Request): [description]
        username (str, optional): [description]. Defaults to Form(...).
        password (str, optional): [description]. Defaults to Form(...).
        confirm_password (str, optional): [description]. Defaults to Form(...).
        db (Session, optional): [description]. Defaults to Depends(get_db).

    Returns:
        [type]: [description]
    """
    if password != confirm_password:
        request.session["message"] = "Пароли не совпадают"
        return RedirectResponse("/signup", status_code=303)

    existing_user = db.query(User).filter(User.username == username).first()
    if existing_user:
        request.session["message"] = "Имя пользователя уже существует."
        return RedirectResponse("/signup", status_code=303)
    hashed_password = User.get_password_hash(password)
    new_user = User(username=username, password=hashed_password)
    db.add(new_user)
    db.commit()
    request.session["message"] = "Вы успешно зарегистрировались!"
    return RedirectResponse("/login", status_code=303)


# Login page route
@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    """AI is creating summary for login_form

    Args:
        request (Request): [description]

    Returns:
        [type]: [description]
    """
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login", response_class=HTMLResponse)
async def process_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    """AI is creating summary for process_login

    Args:
        request (Request): [description]
        username (str, optional): [description]. Defaults to Form(...).
        password (str, optional): [description]. Defaults to Form(...).
        db (Session, optional): [description]. Defaults to Depends(get_db).

    Returns:
        [type]: [description]
    """
    user = db.query(User).filter_by(username=username).first()
    if not user or not User.verify_password(password, user.password):
        request.session["message"] = "Неверное имя пользователя или пароль."
        return RedirectResponse("/login", status_code=303)
    request.session["message"] = "Вы успешно вошли в систему!"
    return RedirectResponse("/admin", status_code=303)


# Admin page route
@app.get("/admin", response_class=HTMLResponse)
async def admin(request: Request):
    """AI is creating summary for admin

    Args:
        request (Request): [description]

    Returns:
        [type]: [description]
    """
    return templates.TemplateResponse("admin.html", {"request": request})
