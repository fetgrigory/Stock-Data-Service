import os
from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from src.auth.service import check_email_exists
from src.auth.schemas import UserCreate
from src.db.crud import get_all_quotes
from . import service

router = APIRouter()

# Templates
templates = Jinja2Templates(directory=os.path.join("src", "templates"))


# Login page route
@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(
        name="login.html",
        context={},
        request=request
    )


# Verifies user credentials and redirects to /user on success, or returns login page with error
@router.post("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    ):
    if await service.verify_user(username, password):
        user = await service.get_user_by_username(username)
        token = service.create_access_token(str(user.id))

        response = RedirectResponse(
            url="/user",
            status_code=302
        )

        service.security.set_access_cookies(
            token,
            response
        )

        return response

    return templates.TemplateResponse(
        name="login.html",
        context={"error": True},
        request=request
    )


# Signup page route
@router.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse(
        name="signup.html",
        context={},
        request=request
    )


# Creates a new user, or returns signup page with error if user already exists
@router.post("/signup", response_class=HTMLResponse)
async def signup(
    request: Request,
    last_name: str = Form(...),
    first_name: str = Form(...),
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    ):
    # Checking if a user with this email already exists
    existing_user = await check_email_exists(email)

    if existing_user:
        return templates.TemplateResponse(
            name="signup.html",
            context={"error": True},
            request=request
        )

    try:
        # Create a new user if the email is unique
        user = UserCreate(
            last_name=last_name,
            first_name=first_name,
            username=username,
            email=email,
            password=password
        )

        await service.create_user(user)

        return RedirectResponse(
            url="/login",
            status_code=302
        )

    except Exception:
        return templates.TemplateResponse(
            name="signup.html",
            context={"error": True},
            request=request
        )


# Renders the protected test page; accessible only with a valid access token
@router.get(
    "/user",
    response_class=HTMLResponse,
    dependencies=[Depends(service.security.access_token_required)]
)
async def user_page(request: Request):
    quotes = await get_all_quotes()

    return templates.TemplateResponse(
        name="user.html",
        context={"quotes": quotes},
        request=request
    )
