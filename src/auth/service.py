import bcrypt
from authx import AuthX, AuthXConfig
from fastapi import Depends, HTTPException
from src.auth.schemas import UserCreate
from src.db.crud import insert_user, get_user_by_username, get_user_by_email, get_user_by_id

# Setting up AuthX
config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]
security = AuthX(config=config)


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


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(
        password.encode(),
        hashed.encode()
    )


# Generates a JWT access token for user authentication based on UID
def create_access_token(uid: str) -> str:
    return security.create_access_token(uid=uid)


# Salt generation and hashing
def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    )
    return hashed.decode()


# Verifies that the user's password matches the hash stored in the database
async def verify_user(username: str, password: str):
    user = await get_user_by_username(username)

    if not user:
        return False

    return verify_password(password, user.password)


# Getting the authenticated user
async def get_current_user(
    token=Depends(security.access_token_required)
):
    user_id = token.uid

    user = await get_user_by_id(
        int(user_id)
    )

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Пользователь не найден"
        )

    return user
