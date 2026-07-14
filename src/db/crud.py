from datetime import datetime, date
from sqlalchemy import select, func
from src.db.database import async_session_factory
from src.db.models import User, Recipient, SmtpSetting, Quote


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


# Getting the user's by username
async def get_user_by_username(username: str):
    async with async_session_factory() as session:
        result = await session.execute(
            select(User).where(User.username == username)
        )

        return result.scalar_one_or_none()


# Getting the user's by email
async def get_user_by_email(email: str):
    async with async_session_factory() as session:
        result = await session.execute(
            select(User).where(User.email == email)
        )

        return result.scalars().first()


# Adding a new recipient
async def insert_recipient(name: str, email: str):
    async with async_session_factory() as session:
        recipient = Recipient(
            name=name,
            email=email
        )

        session.add(recipient)
        await session.commit()

        await session.refresh(recipient)

        recipient_id = recipient.id

    return recipient_id


# Updating a recipient
async def refresh_recipient(
        recipient_id: int,
        name: str | None,
        email: str | None
):
    async with async_session_factory() as session:
        recipient = await session.get(Recipient, recipient_id)

        if not recipient:
            return None

        if name and name.strip():
            recipient.name = name

        if email and email.strip():
            recipient.email = email

        await session.commit()

        return {
            "name": recipient.name,
            "email": recipient.email
        }


# Deleting a recipient
async def delete_recipient(recipient_id: int):
    async with async_session_factory() as session:
        recipient = await session.get(Recipient, recipient_id)

        if recipient:
            await session.delete(recipient)
            await session.commit()

    return recipient_id


# Returns a list of all recipients with id, name, and email
async def get_all_recipients():
    async with async_session_factory() as session:
        result = await session.execute(
            select(Recipient).order_by(Recipient.id.asc())
        )

        recipients = result.scalars().all()

        return [
            {
                "id": r.id,
                "name": r.name,
                "email": r.email
            }
            for r in recipients
        ]


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


# Returns a list of all email addresses of recipients
async def get_all_recipient_emails():
    async with async_session_factory() as session:
        result = await session.execute(
            select(Recipient)
        )

        recipients = result.scalars().all()
        emails = [recipient.email for recipient in recipients]

        return emails


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


# Getting the recipient's name by email
async def get_recipient_name(email: str):
    async with async_session_factory() as session:
        result = await session.execute(
            select(Recipient).where(Recipient.email == email)
        )

        recipient = result.scalars().first()

        return recipient.name if recipient else None


# Inserts a new stock quote into the database
async def insert_quote(
    ticker: str,
    name: str,
    update_time: datetime,
    last_price: float,
    prev_price: float,
    change: float,
    change_percent: float,
    open_price: float,
    high: float,
    low: float,
    volume: int,
    value: float,
    lot_size: int,
):
    async with async_session_factory() as session:
        quote = Quote(
            ticker=ticker,
            name=name,
            update_time=update_time,
            last_price=last_price,
            prev_price=prev_price,
            change=change,
            change_percent=change_percent,
            open=open_price,
            high=high,
            low=low,
            volume=volume,
            value=value,
            lot_size=lot_size
        )

        session.add(quote)
        await session.commit()

        await session.refresh(quote)

        quote_id = quote.id

        return quote_id


# Fetch all stock quotes from the database
async def get_all_quotes():
    async with async_session_factory() as session:
        result = await session.execute(
            select(Quote).order_by(Quote.id.asc())
        )

        quotes = result.scalars().all()

        return [
            {
                "id": q.id,
                "update_time": q.update_time,
                "ticker": q.ticker,
                "name": q.name,
                "last_price": q.last_price,
                "prev_price": q.prev_price,
                "change": q.change,
                "change_percent": q.change_percent,
                "open": q.open,
                "high": q.high,
                "low": q.low,
                "volume": q.volume,
                "value": q.value,
                "lot_size": q.lot_size
            }
            for q in quotes
        ]


# Fetch all stock quotes from the database by date
async def get_quotes(target_date: date | None = None):
    async with async_session_factory() as session:
        query = select(Quote).order_by(Quote.id.asc())

        if target_date is not None:
            query = query.where(
                func.date(Quote.update_time) == target_date
            )

        result = await session.execute(query)
        quotes = result.scalars().all()

        return [
            {
                "id": q.id,
                "update_time": q.update_time,
                "ticker": q.ticker,
                "name": q.name,
                "last_price": q.last_price,
                "prev_price": q.prev_price,
                "change": q.change,
                "change_percent": q.change_percent,
                "open": q.open,
                "high": q.high,
                "low": q.low,
                "volume": q.volume,
                "value": q.value,
                "lot_size": q.lot_size
            }
            for q in quotes
        ]
