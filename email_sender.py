# email_sender.py
import smtplib
import os
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from platform import python_version


class EmailSender:
    def __init__(self):
        self.server = "smtp.mail.com"
        self.user = "info@example.com"
        self.password = "password123"
        self.recipients = "admin@example.com",
        self.sender = "noreply@example.com"
        self.subject = 'Архив с данными'
        self.text = 'Здравствуйте! Во вложении находится архив с актуальными данными.'
        self.html = f'<html><head></head><body><p>{self.text}</p></body></html>'

    def send_email_with_attachment(self, filepath):
        try:
            basename = os.path.basename(filepath)
            filesize = os.path.getsize(filepath)

            msg = MIMEMultipart('alternative')
            msg['Subject'] = self.subject
            msg['From'] = f'Python script <{self.sender}>'
            msg['To'] = ', '.join(self.recipients)
            msg['Reply-To'] = self.sender
            msg['Return-Path'] = self.sender
            msg['X-Mailer'] = f'Python/{python_version()}'

            part_text = MIMEText(self.text, 'plain')
            part_html = MIMEText(self.html, 'html')
            part_file = MIMEBase('application', f'octet-stream; name="{basename}"')
            with open(filepath, "rb") as f:
                part_file.set_payload(f.read())
            part_file.add_header('Content-Description', basename)
            part_file.add_header('Content-Disposition', f'attachment; filename="{basename}"; size={filesize}')
            encoders.encode_base64(part_file)

            msg.attach(part_text)
            msg.attach(part_html)
            msg.attach(part_file)

            with smtplib.SMTP_SSL(self.server) as mail:
                mail.login(self.user, self.password)
                mail.sendmail(self.sender, self.recipients, msg.as_string())

            logging.info("Email sent successfully with attachment: %s", filepath)
            return True
        except Exception as e:
            logging.error("Failed to send email: %s", e)
            return False