'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 07/11/2025
Ending //

'''
# Installing the necessary libraries
from sqlalchemy import insert, select
from src.db.database_orm import engine
from src.db.models import users_table


# Adding a new user
def insert_user(username: str, password: str):
    """AI is creating summary for insert_user

    Args:
        username (str): [description]
        password (str): [description]
    """
    with engine.connect() as conn:
        stmt = insert(users_table).values(username=username, password=password)
        conn.execute(stmt)
        conn.commit()


# Getting the user's by username
def get_user_by_username(username: str):
    """AI is creating summary for get_user_by_username

    Args:
        username (str): [description]

    Returns:
        [type]: [description]
    """
    with engine.connect() as conn:
        stmt = select(users_table).where(users_table.c.username == username)
        result = conn.execute(stmt).first()
        return result
