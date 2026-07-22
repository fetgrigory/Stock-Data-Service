from sqlalchemy import select
from src.db.database import async_session_factory
from src.recipients.models import Recipient


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


# Returns a list of all email addresses of recipients
async def get_all_recipient_emails():
    async with async_session_factory() as session:
        result = await session.execute(
            select(Recipient)
        )

        recipients = result.scalars().all()
        emails = [recipient.email for recipient in recipients]

        return emails


# Getting the recipient's name by email
async def get_recipient_name(email: str):
    async with async_session_factory() as session:
        result = await session.execute(
            select(Recipient).where(Recipient.email == email)
        )

        recipient = result.scalars().first()

        return recipient.name if recipient else None