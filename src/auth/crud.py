from sqlalchemy import select
from src.db.database import async_session_factory
from src.auth.models import User


# Adding a new user
async def insert_user(
        last_name: str,
        first_name: str,
        username: str,
        email: str,
        password: str
        ):
    async with async_session_factory() as session:
        user = User(
            last_name=last_name,
            first_name=first_name,
            username=username,
            email=email,
            password=password
        )

        session.add(user)
        await session.commit()

        await session.refresh(user)

        user_id = user.id
        return user_id


# Updating a user
async def update_user(
        user_id: int,
        last_name: str | None,
        first_name: str | None,
        email: str | None
):
    async with async_session_factory() as session:
        user = await session.get(User, user_id)

        if not user:
            return None

        if last_name and last_name.strip():
            user.last_name = last_name

        if first_name and first_name.strip():
            user.first_name = first_name

        if email and email.strip():
            user.email = email

        await session.commit()

        return {
            "last_name": user.last_name,
            "first_name": user.first_name,
            "email": user.email
        }


# Getting the user's by username
async def get_user_by_username(username: str):
    async with async_session_factory() as session:
        result = await session.execute(
            select(User).where(User.username == username)
        )

        return result.scalar_one_or_none()


# Getting the user's by id
async def get_user_by_id(user_id: int):
    async with async_session_factory() as session:
        result = await session.execute(
            select(User).where(User.id == user_id)
        )

        return result.scalar_one_or_none()


# Getting the user's by email
async def get_user_by_email(email: str):
    async with async_session_factory() as session:
        result = await session.execute(
            select(User).where(User.email == email)
        )

        return result.scalars().first()
