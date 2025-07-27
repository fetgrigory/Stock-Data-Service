'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 25/07/2025
Ending //

'''
# Installing the necessary libraries
import os
from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()

# Templates and statics
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Secret key for flash messages via sessions
app.add_middleware(SessionMiddleware, secret_key="secret_key")

# Database configuration
DATABASE_URL = "sqlite:///./users.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(80), nullable=False)


# Creating tables
Base.metadata.create_all(bind=engine)


# Render main page
@app.get("/", response_class=HTMLResponse)
@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Render about page
@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse("about.html", {"request": request})


# Render signup page
@app.get("/signup", response_class=HTMLResponse)
async def signup_form(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})


@app.post("/signup", response_class=HTMLResponse)
async def signup(request: Request, username: str = Form(...), password: str = Form(...),
                 confirm_password: str = Form(...)):
    db = SessionLocal()
    existing_user = db.query(User).filter(User.username == username).first()

    if password != confirm_password:
        request.session["message"] = "Пароли не совпадают"
        return RedirectResponse("/signup", status_code=303)

    if existing_user:
        request.session["message"] = "Имя пользователя уже существует."
        return RedirectResponse("/signup", status_code=303)

    new_user = User(username=username, password=password)
    db.add(new_user)
    db.commit()
    db.close()
    request.session["message"] = "Вы успешно зарегистрировались!"
    return RedirectResponse("/login", status_code=303)


# Render login page
@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login", response_class=HTMLResponse)
async def login(request: Request, username: str = Form(...), password: str = Form(...)):
    db = SessionLocal()
    user = db.query(User).filter_by(username=username, password=password).first()
    db.close()
    if user:
        request.session["message"] = "Вы успешно вошли в систему!"
        return RedirectResponse("/test", status_code=303)
    else:
        request.session["message"] = "Неверное имя пользователя или пароль."
        return RedirectResponse("/login", status_code=303)


# Render test page
@app.get("/test", response_class=HTMLResponse)
async def test(request: Request):
    return templates.TemplateResponse("test.html", {"request": request})
