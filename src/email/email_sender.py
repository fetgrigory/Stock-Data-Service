'''
This module make

Author: Fetkulin Grigory, Fetkulin.G.R@yandex.ru
Starting 11/07/2025
Ending //

'''
# Installing the necessary libraries
import logging
import os
import smtplib
from datetime import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from platform import python_version
from src.database import get_all_recipients, get_smtp_setting, get_recipient_name


class EmailSender:
    """AI is creating summary for
    """
    def __init__(self):
        # Getting SMTP settings from the database
        smtp_config = get_smtp_setting()
        if not smtp_config:
            raise ValueError("SMTP настройки не найдены в базе данных.")
        self.smtp_id, self.server, self.port, self.user, self.password, self.sender = smtp_config
        self.password = self.password.strip("\n\r\t")
        # Getting a list of recipients
        self.recipients = get_all_recipients()
        if not self.recipients:
            logging.warning("Список получателей пуст!")

        # Send email with file attachment
    def send_email_with_attachment(self, filepath):
        """AI is creating summary for send_email_with_attachment

        Args:
            filepath ([type]): [description]
        """
        basename = os.path.basename(filepath)
        filesize = os.path.getsize(filepath)
        # Dynamic subject and text of the letter
        for recipient_email in self.recipients:
            try:
                # Get the name of a specific recipient
                name = get_recipient_name(recipient_email)
                subject = f'Архив с биржевыми данными от {datetime.now():%d.%m.%Y}'
                text = f'Здравствуйте, {name}! Во вложении находится архив с актуальными данными.'
                html = f'<html><head></head><body><p>{text}</p></body></html>'

                # Create multipart message container
                msg = MIMEMultipart('alternative')
                msg['Subject'] = subject
                msg['From'] = f'Python script <{self.sender}>'
                msg['To'] = recipient_email
                msg['Reply-To'] = self.sender
                msg['Return-Path'] = self.sender
                msg['X-Mailer'] = f'Python/{python_version()}'

                # Create text and HTML email parts
                part_text = MIMEText(text, 'plain')
                part_html = MIMEText(html, 'html')

                # Add file headers
                part_file = MIMEBase('application', f'octet-stream; name="{basename}"')
                with open(filepath, "rb") as f:
                    part_file.set_payload(f.read())
                part_file.add_header('Content-Description', basename)
                part_file.add_header('Content-Disposition', f'attachment; filename="{basename}"; size={filesize}')
                encoders.encode_base64(part_file)

                # Attach all parts to message
                msg.attach(part_text)
                msg.attach(part_html)
                msg.attach(part_file)

                # Send email via SMTP server
                with smtplib.SMTP_SSL(self.server, self.port) as mail:
                    mail.login(self.user, self.password)
                    mail.sendmail(self.sender, recipient_email, msg.as_string())
                logging.info("Email sent successfully to: %s", recipient_email)

            except Exception as e:
                logging.error("Failed to send email to %s: %s", recipient_email, e)
