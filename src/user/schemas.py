from pydantic import BaseModel, EmailStr, field_validator

# Allowed email domains
TRUSTED_DOMAINS = {
    "gmail.com",
    "yandex.ru",
    "mail.ru",
    "outlook.com",
}


# User registration schema
class UserCreate(BaseModel):
    last_name: str
    first_name: str
    username: str
    email: EmailStr
    password: str

    @field_validator("email")
    @classmethod
    def check_trusted_domain(cls, v: EmailStr):
        domain = v.split("@")[-1].lower()
        if domain not in TRUSTED_DOMAINS:
            raise ValueError("Email domain is not allowed")
        return v
