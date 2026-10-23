import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate, make_msgid

import aiosmtplib

from src.email.crud import get_smtp_setting

logger = logging.getLogger(__name__)

SMTP_TIMEOUT = 15
SMTP_SSL_PORT = 465

WELCOME_SUBJECT = "Регистрация"
WELCOME_TEXT = "Вы успешно зарегистрированы!"


# Get SMTP settings from the database
async def _get_smtp_params():
    smtp_config = await get_smtp_setting()
    if not smtp_config:
        raise ValueError("SMTP settings not found in the database.")

    port = int(smtp_config.port)
    sender = smtp_config.sender
    username = getattr(smtp_config, "username", sender)

    if sender != username:
        logger.warning(
            "Sender address (%s) does not match SMTP login (%s): "
            "many providers reject such emails",
            sender,
            username,
        )

    use_ssl = port == SMTP_SSL_PORT
    params = {
        "hostname": smtp_config.server,
        "port": port,
        "username": username,
        "password": smtp_config.password.strip("\n\r\t"),
        "use_tls": use_ssl,
        "start_tls": not use_ssl,
        "timeout": SMTP_TIMEOUT,
    }
    return params, sender


# Create text and HTML email parts
def _build_message(
    sender: str,
    recipient: str,
    subject: str,
    plain_content: str,
):
    text = plain_content or WELCOME_TEXT

    message = MIMEMultipart("alternative")
    message["From"] = sender
    message["To"] = recipient
    message["Subject"] = subject
    message["Date"] = formatdate(localtime=True)
    message["Message-ID"] = make_msgid()

    message.attach(MIMEText(text, "plain", "utf-8"))
    message.attach(
        MIMEText(f"<html><body><p>{text}</p></body></html>", "html", "utf-8")
    )
    return message


# Send an email via the SMTP server
async def send_email(
    recipient: str,
    subject: str,
    plain_content: str = "",
):
    logger.info("Starting to send email to %s", recipient)

    params, sender = await _get_smtp_params()

    logger.info(
        "SMTP: server=%s, port=%s, use_tls=%s, start_tls=%s",
        params["hostname"],
        params["port"],
        params["use_tls"],
        params["start_tls"],
    )

    message = _build_message(
        sender=sender,
        recipient=recipient,
        subject=subject,
        plain_content=plain_content,
    )

    await aiosmtplib.send(message, **params)
    logger.info("Email handed over to the SMTP server for %s", recipient)


# Send a welcome email, logging errors instead of raising
async def send_welcome_email(email: str):
    try:
        await send_email(recipient=email, subject=WELCOME_SUBJECT)
    except Exception:
        logger.exception("Failed to send email to %s", email)
