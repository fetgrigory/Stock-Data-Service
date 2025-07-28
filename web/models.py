'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 27/07/2025
Ending //

'''
# Installing the necessary libraries
from passlib.context import CryptContext
from sqlalchemy import Column, Integer, String
from .database import Base

# Creating a context for hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(Base):
    """AI is creating summary for User

    Args:
        Base ([type]): [description]
    """
    __tablename__ = "users"
    # id (int): Unique identifier for each user
    id = Column(Integer, primary_key=True, index=True)
    # Username, required for login
    username = Column(String(80), unique=True, nullable=False)
    # User's password
    password = Column(String(128), nullable=False)

    # Hashes the provided password
    @staticmethod
    def get_password_hash(password: str) -> str:
        """AI is creating summary for get_password_hash

        Args:
            password (str): [description]

        Returns:
            str: [description]
        """
        return pwd_context.hash(password)

    # Checks if the password matches the hash
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """AI is creating summary for verify_password

        Args:
            plain_password (str): [description]
            hashed_password (str): [description]

        Returns:
            bool: [description]
        """
        return pwd_context.verify(plain_password, hashed_password)
