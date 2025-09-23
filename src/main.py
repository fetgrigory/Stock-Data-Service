'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 23/09/2025
Ending //

'''
# Installing the necessary libraries
from fastapi import FastAPI
import uvicorn
from pydantic import BaseModel

app = FastAPI()


# User data model with name and email fields
class User(BaseModel):
    name: str
    email: str


# Endpoint for adding a new user
@app.post(
    "/users",
    tags=["Пользователи 👤"],
    summary="Добавить нового пользователя"
)
# Return the name and email
def create_user(user: User):
    return {"Имя": user.name, "Адрес электронной почты": user.email}


if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=80, reload=True)
