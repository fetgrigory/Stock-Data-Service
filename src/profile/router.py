import os
from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.exc import IntegrityError
from src.auth.service import get_current_user
from src.db.crud import refresh_user

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
        name="profile.html",
        context={
            "user": user
        },
        request=request
    )


# Endpoint for update user profile
@router.post(
    "/profile/update",
    tags=["Профиль 👤"],
    summary="Обновить данные пользователя",
    status_code=200
)
async def update_user(
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

        return {
            "id": current_user.id,
            "Фамилия": updated_user["last_name"],
            "Имя": updated_user["first_name"],
            "Email": updated_user["email"]
        }

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
