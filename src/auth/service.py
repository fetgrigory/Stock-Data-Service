
import bcrypt
from authx import AuthX, AuthXConfig
from fastapi import Depends, HTTPException

from src.user.crud import (
    get_user_by_username,
    get_user_by_id,
)

# Setting up AuthX
config = AuthXConfig()
config.JWT_SECRET_KEY = "SECRET_KEY"
config.JWT_ACCESS_COOKIE_NAME = "my_access_token"
config.JWT_TOKEN_LOCATION = ["cookies"]
config.JWT_COOKIE_CSRF_PROTECT = False

security = AuthX(config=config)


def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())


def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed.decode()


def create_access_token(user_id: str) -> str:
    return security.create_access_token(uid=user_id)


# Verifies the password hash
async def verify_user(username: str, password: str):
    user = await get_user_by_username(username)

    if not user:
        return False

    return verify_password(password, user.password)


# Getting the authenticated user
async def get_current_user(
    token=Depends(security.access_token_required)
):
    user_id = token.sub
    user = await get_user_by_id(int(user_id))

    if not user:
        raise HTTPException(
            status_code=404,
            detail="Пользователь не найден"
        )

    return user
