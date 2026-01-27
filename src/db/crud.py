'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 07/11/2025
Ending //

'''
# Installing the necessary libraries
from datetime import datetime
from src.db.database import session_factory
from src.db.models import User, Recipient, SmtpSetting, Quote


# Adding a new user
def insert_user(username: str, email: str, password: str):
    """AI is creating summary for insert_user

    Args:
        username (str): [description]
        password (str): [description]
    """
    with session_factory() as session:
        user = User(username=username, email=email, password=password)
        session.add(user)
        session.commit()
        user_id = user.id
        return user_id


# Getting the user's by username
def get_user_by_username(username: str):
    """AI is creating summary for get_user_by_username

    Args:
        username (str): [description]

    Returns:
        [type]: [description]
    """
    with session_factory() as session:
        return session.query(User).filter(User.username == username).first()


# Getting the user's by email
def get_user_by_email(email: str):
    """AI is creating summary for get_user_by_email

    Args:
        email (str): [description]

    Returns:
        [type]: [description]
    """
    with session_factory() as session:
        return session.query(User).filter(User.email == email).first()


# Adding a new recipient
def insert_recipient(name: str, email: str):
    """AI is creating summary for insert_recipient

    Args:
        name (str): [description]
        email (str): [description]

    Returns:
        [type]: [description]
    """
    with session_factory() as session:
        recipient = Recipient(name=name, email=email)
        session.add(recipient)
        session.commit()
        recipient_id = recipient.id
    return recipient_id


# Updating a recipient
def refresh_recipient(recipient_id: int, name: str | None, email: str | None):
    """AI is creating summary for update_recipient_data

    Args:
        recipient_id (int): [description]
        name (str): [description]
        email (str): [description]

    Returns:
        [type]: [description]
    """
    with session_factory() as session:
        recipient = session.get(Recipient, recipient_id)
        if not recipient:
            return None

        # Update the field if given, else retain current
        if name and name.strip():
            recipient.name = name
        if email and email.strip():
            recipient.email = email

        session.commit()
        return {"name": recipient.name, "email": recipient.email}


# Deleting a recipient
def delete_recipient(recipient_id: int):
    """AI is creating summary for delete_recipient

    Args:
        recipient_id (int): [description]

    Returns:
        [type]: [description]
    """
    with session_factory() as session:
        recipient = session.get(Recipient, recipient_id)
        if recipient:
            session.delete(recipient)
            session.commit()
    return recipient_id


# Returns a list of all recipients with id, name, and email
def get_all_recipients():
    """AI is creating summary for get_all_recipients

    Returns:
        [type]: [description]
    """
    with session_factory() as session:
        recipients = session.query(Recipient).order_by(Recipient.id.asc()).all()
        return [{"id": r.id, "name": r.name, "email": r.email} for r in recipients]


# Add a new configuration
def insert_smtp_setting(
        server: str,
        port: int,
        username: str,
        password: str,
        sender: str
        ) -> int:
    """AI is creating summary for insert_smtp_setting

    Args:
        server (str): [description]
        port (int): [description]
        username (str): [description]
        password (str): [description]
        sender (str): [description]

    Returns:
        int: [description]
    """
    with session_factory() as session:
        smtp_setting = SmtpSetting(
            server=server,
            port=port,
            username=username,
            password=password,
            sender=sender
        )
        session.add(smtp_setting)
        session.commit()
        return smtp_setting.id


# Get the first configuration
def get_smtp_setting():
    """AI is creating summary for get_smtp_setting

    Returns:
        [type]: [description]
    """
    with session_factory() as session:
        smtp_setting = session.query(SmtpSetting).first()
        return smtp_setting


# Returns a list of all email addresses of recipients
def get_all_recipient_emails():
    """AI is creating summary for get_all_recipient_emails

    Returns:
        [type]: [description]
    """
    with session_factory() as session:
        recipients = session.query(Recipient).all()
        emails = [recipient.email for recipient in recipients]
        return emails


# Updating a configuration
def update_smtp_setting(
    smtp_id: int,
    server: str | None,
    port: int | None,
    username: str | None,
    password: str | None,
    sender: str | None,
):
    """AI is creating summary for update_smtp_setting_data

    Args:
        smtp_id (int): [description]
        server (str): [description]
        port (int): [description]
        username (str): [description]
        password (str): [description]
        sender (str): [description]

    Returns:
        [type]: [description]
    """
    with session_factory() as session:
        # Getting the current record
        smtp_setting = session.get(SmtpSetting, smtp_id)
        if not smtp_setting:
            return None
    # Update fields only if a new value is passed
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

        session.commit()

        updated_data = {
            "server": smtp_setting.server,
            "port": smtp_setting.port,
            "username": smtp_setting.username,
            "password": smtp_setting.password,
            "sender": smtp_setting.sender
        }
        return updated_data


# Deleting a configuration
def delete_smtp_setting(smtp_id: int):
    """AI is creating summary for delete_smtp_setting_data

    Args:
        smtp_id (int): [description]

    Returns:
        [type]: [description]
    """
    with session_factory() as session:
        smtp_setting = session.get(SmtpSetting, smtp_id)
        if smtp_setting:
            session.delete(smtp_setting)
            session.commit()
        return smtp_id


# Getting the recipient's name by email
def get_recipient_name(email: str):
    """AI is creating summary for get_recipient_name

    Args:
        email (str): [description]

    Returns:
        [type]: [description]
    """
    with session_factory() as session:
        recipient = session.query(Recipient).filter(Recipient.email == email).first()
        return recipient.name if recipient else None


# Inserts a new stock quote into the database
def insert_quote(
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
    """AI is creating summary for insert_quote

    Args:
        ticker (str): [description]
        name (str): [description]
        update_time (datetime): [description]
        last_price (float): [description]
        prev_price (float): [description]
        change (float): [description]
        change_percent (float): [description]
        open (float): [description]
        high (float): [description]
        low (float): [description]
        volume (int): [description]
        value (float): [description]
        lot_size (int): [description]

    Returns:
        [type]: [description]
    """
    with session_factory() as session:
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
        session.commit()
        quote_id = quote.id
        return quote_id


# Fetch all stock quotes from the database
def get_all_quotes():
    with session_factory() as session:
        quotes = session.query(Quote).order_by(Quote.id.asc()).all()
        return [
            {
                "id": q.id,
                "ticker": q.ticker,
                "trade_time": q.trade_time,
                "last_price": q.last_price,
                "change_abs": q.change_abs,
                "change_percent": q.change_percent,
                "price_before_closing": q.price_before_closing,
                "price_at_opening": q.price_at_opening,
                "minimum_price": q.minimum_price,
                "average_overpriced": q.average_overpriced,
                "pieces_per_day": q.pieces_per_day,
                "quantity_per_day": q.quantity_per_day,
                "rub": q.rub,
                "num_transactions_per_day": q.num_transactions_per_day
            }
            for q in quotes
        ]
