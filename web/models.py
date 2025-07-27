'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 27/07/2025
Ending //

'''
# Installing the necessary libraries
from sqlalchemy import Column, Integer, String
from .database import Base


class User(Base):
    """AI is creating summary for User

    Args:
        Base ([type]): [description]
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(80), unique=True, nullable=False)
    password = Column(String(80), nullable=False)
