'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 07/11/2025
Ending //

'''
# Installing the necessary libraries
from sqlalchemy.orm import Session
from src.db.database_orm import engine
from src.db.models import User


# Adding a new user
def insert_user(username: str, password: str):
    """AI is creating summary for insert_user

    Args:
        username (str): [description]
        password (str): [description]
    """
    with Session(engine) as session:
        user = User(username=username, password=password)
        session.add(user)
        session.commit()


# Getting the user's by username
def get_user_by_username(username: str):
    """AI is creating summary for get_user_by_username

    Args:
        username (str): [description]

    Returns:
        [type]: [description]
    """
    with Session(engine) as session:
        return session.query(User).filter(User.username == username).first()
