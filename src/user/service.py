from src.auth.service import hash_password
from src.user.schemas import UserCreate
from src.user.crud import insert_user, get_user_by_email


# Creates a new user with a hashed password
async def create_user(user: UserCreate):
    hashed = hash_password(user.password)

    return await insert_user(
        user.last_name,
        user.first_name,
        user.username,
        user.email,
        hashed
    )


# Checking if a user with this email exists
async def check_email_exists(email: str):
    return await get_user_by_email(email)
