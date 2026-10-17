
import os

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from src.quotes.crud import get_all_quotes
from src.auth import service

router = APIRouter()
templates = Jinja2Templates(directory=os.path.join("src", "templates"))


# Login page route
@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(
        name="login.html", context={}, request=request
    )


# Authenticates user and redirects on success
@router.post("/login", response_class=HTMLResponse)
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
):
    if await service.verify_user(username, password):
        user = await service.get_user_by_username(username)
        token = service.create_access_token(str(user.id))

        response = RedirectResponse(url="/user", status_code=302)
        service.security.set_access_cookies(token, response)
        return response

    return templates.TemplateResponse(
        name="login.html", context={"error": True}, request=request
    )


@router.get(
    "/user",
    response_class=HTMLResponse,
    dependencies=[Depends(service.security.access_token_required)],
)
async def user_page(request: Request):
    quotes = await get_all_quotes()
    return templates.TemplateResponse(
        name="user.html",
        context={"quotes": quotes},
        request=request,
    )
