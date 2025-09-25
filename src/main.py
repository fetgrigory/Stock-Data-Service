'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 23/09/2025
Ending //

'''
# Installing the necessary libraries
import os
import psycopg2
from psycopg2 import errorcodes
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# User data model with name and email fields
class User(BaseModel):
    name: str
    email: str


def db_connect():
    """AI is creating summary for db_connect

    Returns:
        [type]: [description]
    """
    # Establish a connection to the PostgreSQL database using environment variables
    return psycopg2.connect(
        # Database host
        host=os.getenv('HOST'),
        # Name of the database
        dbname=os.getenv('DBNAME'),
        # Username for authentication
        user=os.getenv('USER'),
        # Password for authentication
        password=os.getenv('PASSWORD'),
        # Port number for database connection
        port=os.getenv('PORT')
    )


# Creates the users table if it does not exist
def create_users_table():
    with db_connect() as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE
                )
            """)
        conn.commit()


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
        with db_connect() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING id",
                    (user.name, user.email)
                )
                user_id = cursor.fetchone()[0]
            conn.commit()
        return {"id": user_id, "Имя": user.name, "Адрес электронной почты": user.email}

    except psycopg2.Error as e:
        if e.pgcode == errorcodes.UNIQUE_VIOLATION:
            raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует") from e
        else:
            raise


if __name__ == "__main__":
    uvicorn.run("main:app", host='127.0.0.1', port=8000, reload=True)
