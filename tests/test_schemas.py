'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 07/02/2026
Ending //

'''
# Installing the necessary libraries
from src.auth.schemas import UserCreate


def test_user_create_with_trusted_email():
    # Create test data
    username = "testuser"
    email = "test@gmail.com"

    # Create UserCreate object (Pydantic will validate the email)
    user = UserCreate(username=username, email=email, password="")

    # Сhecking the result
    assert user.username == username
    assert user.email == email
