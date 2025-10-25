'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 30/09/2025
Ending //

'''
# Installing the necessary libraries
from fastapi import APIRouter, Path, Query, HTTPException
import psycopg2
from psycopg2 import errorcodes
from src.db.database import insert_smtp_setting, update_smtp_data, delete_smtp_data

router = APIRouter(tags=["SMTP Настройки ⚙️"])


# Endpoint for adding a new smtp settings
@router.post(
    "/smtp-settings",
    tags=["SMTP Настройки ⚙️"],
    summary="Добавить SMTP настройки",
    status_code=201
)
def create_smtp_settings(
    server: str = Query(..., description="SMTP сервер"),
    port: int = Query(..., description="Порт"),
    username: str = Query(..., description="Имя пользователя"),
    password: str = Query(..., description="Пароль"),
    sender: str = Query(..., description="Email отправителя")
):
    try:
        smtp_id = insert_smtp_setting(server, port, username, password, sender)
        return {"id": smtp_id, "server": server, "port": port, "username": username, "sender": sender}

    except psycopg2.Error as e:
        if e.pgcode == errorcodes.UNIQUE_VIOLATION:
            raise HTTPException(status_code=400, detail="Такая конфигурация настроек уже существует") from e
        else:
            raise HTTPException(status_code=500, detail="Ошибка сервера") from e


# Endpoint for updating SMTP settings
@router.patch(
    "/smtp-settings/{smtp_id}",
    tags=["SMTP Настройки ⚙️"],
    summary="Обновить SMTP настройки",
    status_code=200
)
def update_smtp_settings(
    smtp_id: int = Path(..., description="ID SMTP настройки для обновления"),
    server: str | None = Query(None, description="Новый SMTP сервер"),
    port: int | None = Query(None, description="Новый порт"),
    username: str | None = Query(None, description="Новое имя пользователя"),
    password: str | None = Query(None, description="Новый пароль"),
    sender: str | None = Query(None, description="Новый email отправителя")
):
    if all(field is None for field in [server, port, username, password, sender]):
        raise HTTPException(status_code=400, detail="Необходимо указать хотя бы одно поле для обновления")
    try:
        updated_smtp = update_smtp_data(smtp_id, server, port, username, password, sender)
        if not updated_smtp:
            raise HTTPException(status_code=404, detail="SMTP настройка не найдена")
        return {"id": smtp_id, "server": updated_smtp["server"], "port": updated_smtp["port"], "username": updated_smtp["username"], "sender": updated_smtp["sender"]}

    except psycopg2.Error as e:
        if e.pgcode == errorcodes.UNIQUE_VIOLATION:
            raise HTTPException(status_code=400, detail="SMTP с таким email отправителя уже существует") from e
        else:
            raise HTTPException(status_code=500, detail="Ошибка сервера") from e


# Endpoint for deleting a SMTP settings
@router.delete(
    "/smtp-settings/{smtp_id}",
    tags=["SMTP Настройки ⚙️"],
    summary="Удалить SMTP настройки",
    status_code=200
)
def delete_smtp_settings(smtp_id: int = Path(..., description="ID SMTP настройки для для удаления")):
    deleted_count = delete_smtp_data(smtp_id)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="SMTP настройка не найдена")
    return {"message": f"SMTP с ID {smtp_id} успешно удален"}
