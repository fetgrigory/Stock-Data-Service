'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 23/09/2025
Ending //

'''
# Installing the necessary libraries
import psycopg2
import uvicorn
from fastapi import FastAPI, Path, Form, HTTPException
from psycopg2 import errorcodes
from database import create_users_table, insert_user, delete_user

app = FastAPI()
# Creating a table at the start of the application
create_users_table()


# Endpoint for adding a new user
@app.post(
    "/users",
    tags=["Пользователи 👤"],
    summary="Добавить нового пользователя",
    status_code=201
)
# Return the name and email
def create_user(
    name: str = Form(..., description="Имя пользователя"),
    email: str = Form(..., description="Email пользователя")
):
    try:
        user_id = insert_user(name, email)
        return {"id": user_id, "Имя": name, "Адрес электронной почты": email}

    except psycopg2.Error as e:
        if e.pgcode == errorcodes.UNIQUE_VIOLATION:
            raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует") from e
        else:
            raise


# Endpoint for deleting a user by ID
@app.delete(
    "/users/{user_id}",
    tags=["Пользователи 👤"],
    summary="Удалить пользователя по ID",
    status_code=200
)
# Return a message confirming the deletion of the user
def remove_user(user_id: int = Path(..., description="ID пользователя для удаления")):
    deleted_count = delete_user(user_id)
    if deleted_count == 0:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return {"message": f"Пользователь с ID {user_id} успешно удален"}


if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)
