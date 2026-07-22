from pathlib import Path as SysPath
from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.exc import IntegrityError
from src.recipients.crud import (
    insert_recipient,
    update_recipient,
    delete_recipient,
    get_all_recipients
)

router = APIRouter(tags=["Пользователи 👤"])

# The absolute path to the templates folder
BASE_DIR = SysPath(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


# Endpoint for adding a new recipient
@router.get("/user")
def get_recipient_form(request: Request):
    # List of current recipients
    recipients = get_all_recipients()
    return templates.TemplateResponse("user.html", {"request": request, "recipients": recipients})


@router.post("/user", response_class=HTMLResponse)
def create_recipient(
    request: Request,
    name: str = Form(..., description="Имя получателя"),
    email: str = Form(..., description="Email получателя")
):
    try:
        insert_recipient(name, email)
        recipients = get_all_recipients()
        return templates.TemplateResponse("user.html", {"request": request, "success": True, "name": name, "email": email, "recipients": recipients})
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Получатель с таким email уже существует") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ошибка сервера") from e


# Endpoint for update recipient
@router.post(
    "/user/update",
    tags=["Получатели 👤"],
    summary="Обновить данные получателя",
    status_code=200
)
def update_recipient_route(
    recipient_id: int = Form(..., description="ID получателя для обновления"),
    name: str | None = Form(None, description="Новое имя получателя"),
    email: str | None = Form(None, description="Новый email получателя")
):
    if name is None and email is None:
        raise HTTPException(status_code=400, detail="Необходимо указать хотя бы одно поле для обновления")
    try:
        updated_recipient = update_recipient(recipient_id, name, email)
        if not updated_recipient:
            raise HTTPException(status_code=404, detail="Получатель не найден")
        return {"id": recipient_id, "Имя": updated_recipient["name"], "Email": updated_recipient["email"]}
    except IntegrityError as e:
        raise HTTPException(status_code=400, detail="Получатель с таким email уже существует") from e
    except Exception as e:
        raise HTTPException(status_code=500, detail="Ошибка сервера") from e


# Endpoint for deleting a recipient by ID
@router.post(
    "/recipients/delete",
    tags=["Получатели 👤"],
    summary="Удалить получателя по ID через форму",
    status_code=200
)
def delete_recipient_form(recipient_id: int = Form(..., description="ID получателя для удаления")):
    deleted_count = delete_recipient(recipient_id)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Получатель не найден")
    return {"message": f"Получатель с ID {recipient_id} успешно удален"}
