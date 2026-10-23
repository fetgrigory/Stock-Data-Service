import logging
import os

from fastapi import APIRouter, BackgroundTasks, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from src.email.service import send_welcome_email
from src.user.schemas import UserCreate
from src.user.service import create_user, check_email_exists

logger = logging.getLogger(__name__)

router = APIRouter()
templates = Jinja2Templates(directory=os.path.join("src", "templates"))


# Signup page route
@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse(
        name="signup.html", context={}, request=request
    )


# Creates a new user or returns an error
@router.post("/signup", response_class=HTMLResponse)
async def signup(
    request: Request,
    background_tasks: BackgroundTasks,
    last_name: str = Form(...),
    first_name: str = Form(...),
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
):
    existing_user = await check_email_exists(email)

    if existing_user:
        logger.info("Registration rejected: email %s already exists", email)
        return templates.TemplateResponse(
            name="signup.html", context={"error": True}, request=request
        )

    try:
        user = UserCreate(
            last_name=last_name,
            first_name=first_name,
            username=username,
            email=email,
            password=password,
        )
        await create_user(user)
        logger.info("User %s created", email)

    except Exception:
        logger.exception("User registration error %s", email)
        return templates.TemplateResponse(
            name="signup.html", context={"error": True}, request=request
        )

    background_tasks.add_task(send_welcome_email, email)

    return RedirectResponse(url="/login", status_code=302)