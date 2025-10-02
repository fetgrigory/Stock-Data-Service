'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 02/10/2025
Ending //

'''
# Installing the necessary libraries
import hashlib
from authx import AuthX, AuthXConfig
from src.database import insert_user, get_user_by_username

# Setting up AuthX
config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]
security = AuthX(config=config)


# Creates a new user with a hashed password
def create_user(username: str, password: str):
    """AI is creating summary for create_user

    Args:
        username (str): [description]
        password (str): [description]

    Returns:
        [type]: [description]
    """
    hashed = hash_password(password)
    return insert_user(username, hashed)


# Hashes the password using SHA-256
def hash_password(password: str) -> str:
    """AI is creating summary for hash_password

    Args:
        password (str): [description]

    Returns:
        str: [description]
    """
    return hashlib.sha256(password.encode()).hexdigest()


# Verifies that the user's password matches the hash stored in the database
def verify_user(username: str, password: str) -> bool:
    """AI is creating summary for verify_user

    Args:
        username (str): [description]
        password (str): [description]

    Returns:
        bool: [description]
    """
    user = get_user_by_username(username)
    if not user:
        return False
    return user[2] == hash_password(password)


# Generates a JWT access token for user authentication based on UID
def create_access_token(uid: str) -> str:
    """AI is creating summary for create_access_token

    Args:
        uid (str): [description]

    Returns:
        str: [description]
    """
    return security.create_access_token(uid=uid)
