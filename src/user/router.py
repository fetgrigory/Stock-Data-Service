
import os

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from src.user.schemas import UserCreate
from src.user.service import create_user, check_email_exists

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
    last_name: str = Form(...),
    first_name: str = Form(...),
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
):
    existing_user = await check_email_exists(email)

    if existing_user:
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

        return RedirectResponse(url="/login", status_code=302)

    except Exception:
        return templates.TemplateResponse(
            name="signup.html", context={"error": True}, request=request
        )
