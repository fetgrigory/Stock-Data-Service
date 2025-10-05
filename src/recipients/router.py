'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 30/09/2025
Ending //

'''
# Installing the necessary libraries
from fastapi import APIRouter, Path, Query, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
import psycopg2
from psycopg2 import errorcodes
from src.database import insert_recipient_data, update_recipient_data, delete_recipient_data

router = APIRouter(tags=["Пользователи 👤"])
templates = Jinja2Templates(directory="templates")


# Endpoint for adding a new recipient
@router.get("/recipients")
def get_recipient_form(request: Request):
    # List of current recipients
    recipients = get_all_recipients()
    return templates.TemplateResponse("recipients.html", {"request": request, "recipients": recipients})


@router.post("/recipients")
def create_recipient(
    name: str = Form(..., description="Имя получателя"),
    email: str = Form(..., description="Email получателя")
):
    try:
        recipient_id = insert_recipient_data(name, email)
        return {"id": recipient_id, "Имя": name, "Email": email}
    except psycopg2.Error as e:
        if e.pgcode == errorcodes.UNIQUE_VIOLATION:
            raise HTTPException(status_code=400, detail="Получатель с таким email уже существует") from e
        else:
            raise


# Endpoint for update recipient
@router.patch(
    "/recipients/{recipient_id}",
    tags=["Получатели 👤"],
    summary="Обновить данные получателя",
    status_code=200
)
def update_recipient(
    recipient_id: int = Path(..., description="ID получателя для обновления"),
    name: str | None = Query(None, description="Новое имя получателя"),
    email: str | None = Query(None, description="Новый email получателя")
):
    if name is None and email is None:
        raise HTTPException(status_code=400, detail="Необходимо указать хотя бы одно поле для обновления")
    try:
        updated_recipient = update_recipient_data(recipient_id, name, email)
        if not updated_recipient:
            raise HTTPException(status_code=404, detail="Получатель не найден")
        return {"id": recipient_id, "Имя": updated_recipient["name"], "Email": updated_recipient["email"]}

    except psycopg2.Error as e:
        if e.pgcode == errorcodes.UNIQUE_VIOLATION:
            raise HTTPException(status_code=400, detail="Получатель с таким email уже существует") from e
        else:
            raise


# Endpoint for deleting a recipient by ID
@router.delete(
    "/recipients/{recipient_id}",
    tags=["Получатели 👤"],
    summary="Удалить получателя по ID",
    status_code=200
)
def delete_recipient(recipient_id: int = Path(..., description="ID получателя для удаления")):
    deleted_count = delete_recipient_data(recipient_id)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Получатель не найден")
    return {"message": f"Получатель с ID {recipient_id} успешно удален"}
