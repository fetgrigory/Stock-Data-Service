'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 17/12/2025
Ending //

'''
# Installing the necessary libraries
from pydantic import BaseModel, EmailStr, field_validator

# Whitelist of allowed email domains
TRUSTED_DOMAINS = {
    "gmail.com",
    "yandex.ru",
    "mail.ru",
    "outlook.com",
}


class UserCreate(BaseModel):
    """AI is creating summary for UserCreate

    Args:
        BaseModel ([type]): [description]

    Raises:
        ValueError: [description]

    Returns:
        [type]: [description]
    """
    # User registration data
    username: str
    email: EmailStr
    password: str

    @field_validator("email")
    @classmethod
    def check_trusted_domain(cls, v: EmailStr):
        """AI is creating summary for check_trusted_domain

        Args:
            v (EmailStr): [description]

        Raises:
            ValueError: [description]

        Returns:
            [type]: [description]
        """
        # Validate that email domain is trusted
        domain = v.split("@")[-1].lower()
        if domain not in TRUSTED_DOMAINS:
            raise ValueError("Email domain is not allowed")
        return v
