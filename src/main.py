'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 23/09/2025
Ending //

'''
# Installing the necessary libraries
import psycopg2
import uvicorn
from fastapi import FastAPI, HTTPException
from psycopg2 import errorcodes
from pydantic import BaseModel
from database import create_users_table, insert_user

app = FastAPI()


# User data model with name and email fields
class User(BaseModel):
    name: str
    email: str


# Creating a table at the start of the application
create_users_table()


# Endpoint for adding a new user
@app.post(
    "/users",
    tags=["Пользователи 👤"],
    summary="Добавить нового пользователя"
)
# Return the name and email
def create_user(user: User):
    try:
        user_id = insert_user(user.name, user.email)
        return {"id": user_id, "Имя": user.name, "Адрес электронной почты": user.email}

    except psycopg2.Error as e:
        if e.pgcode == errorcodes.UNIQUE_VIOLATION:
            raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует") from e
        else:
            raise


if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)
