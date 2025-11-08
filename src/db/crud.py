'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 07/11/2025
Ending //

'''
# Installing the necessary libraries
from sqlalchemy.orm import Session
from src.db.database_orm import engine
from src.db.models import User, Recipient


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
        user_id = user.id
        return user_id


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


# Adding a new recipient
def insert_recipient(name: str, email: str):
    """AI is creating summary for insert_recipient

    Args:
        name (str): [description]
        email (str): [description]

    Returns:
        [type]: [description]
    """
    with Session(engine) as session:
        recipient = Recipient(name=name, email=email)
        session.add(recipient)
        session.commit()
        recipient_id = recipient.id
    return recipient_id
