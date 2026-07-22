import os
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import IntegrityError
from src.auth.service import get_current_user
from src.auth.crud import refresh_user

router = APIRouter()

# Templates
templates = Jinja2Templates(directory=os.path.join("src", "templates"))


# Profile page route
@router.get("/profile", response_class=HTMLResponse)
async def profile(
    request: Request,
    user=Depends(get_current_user)
):
    return templates.TemplateResponse(
        request=request,
        name="profile.html",
        context={
            "user": user
        },
    )


# Endpoint for update user profile
@router.post(
    "/profile/update",
    tags=["Профиль 👤"],
    summary="Обновить данные пользователя",
    response_class=HTMLResponse
)
async def update_user(
    request: Request,
    last_name: str | None = Form(None, description="Новая фамилия пользователя"),
    first_name: str | None = Form(None, description="Новое имя пользователя"),
    email: str | None = Form(None, description="Новый email пользователя"),
    current_user=Depends(get_current_user)
):

    if not any([last_name, first_name, email]):
        raise HTTPException(
            status_code=400,
            detail="Необходимо указать хотя бы одно поле для обновления"
        )

    try:
        updated_user = await refresh_user(
            current_user.id,
            last_name,
            first_name,
            email
        )

        if not updated_user:
            raise HTTPException(
                status_code=404,
                detail="Пользователь не найден"
            )

        return templates.TemplateResponse(
            request=request,
            name="profile.html",
            context={
                "user": updated_user,
                "success_message": "Данные профиля успешно обновлены!"
            }
        )

    except IntegrityError as e:
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким email уже существует"
        ) from e

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Ошибка сервера"
        ) from e
