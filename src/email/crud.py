from sqlalchemy import select
from src.db.database import async_session_factory
from src.email.models import SmtpSetting


# Add a new configuration
async def insert_smtp_setting(
        server: str,
        port: int,
        username: str,
        password: str,
        sender: str
) -> int:
    async with async_session_factory() as session:
        smtp_setting = SmtpSetting(
            server=server,
            port=port,
            username=username,
            password=password,
            sender=sender
        )

        session.add(smtp_setting)
        await session.commit()

        await session.refresh(smtp_setting)

        return smtp_setting.id


# Get the first configuration
async def get_smtp_setting():
    async with async_session_factory() as session:
        result = await session.execute(
            select(SmtpSetting)
        )

        smtp_setting = result.scalars().first()

        return smtp_setting


# Updating a configuration
async def update_smtp_setting(
    smtp_id: int,
    server: str | None,
    port: int | None,
    username: str | None,
    password: str | None,
    sender: str | None,
):
    async with async_session_factory() as session:
        smtp_setting = await session.get(SmtpSetting, smtp_id)

        if not smtp_setting:
            return None

        if server is not None:
            smtp_setting.server = server

        if port is not None:
            smtp_setting.port = port

        if username is not None:
            smtp_setting.username = username

        if password is not None:
            smtp_setting.password = password

        if sender is not None:
            smtp_setting.sender = sender

        await session.commit()

        updated_data = {
            "server": smtp_setting.server,
            "port": smtp_setting.port,
            "username": smtp_setting.username,
            "password": smtp_setting.password,
            "sender": smtp_setting.sender
        }

        return updated_data


# Deleting a configuration
async def delete_smtp_setting(smtp_id: int):
    async with async_session_factory() as session:
        smtp_setting = await session.get(SmtpSetting, smtp_id)

        if smtp_setting:
            await session.delete(smtp_setting)
            await session.commit()

        return smtp_id