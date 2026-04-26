import smtplib
from email.message import EmailMessage

from app.config import get_settings


class GmailService:
    def __init__(self) -> None:
        settings = get_settings()
        self.sender_email = settings.gmail_sender_email
        self.app_password = settings.gmail_app_password

    def send_email(self, recipient: str, subject: str, body: str) -> None:
        message = EmailMessage()
        message["From"] = self.sender_email
        message["To"] = recipient
        message["Subject"] = subject
        message.set_content(body)

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(self.sender_email, self.app_password)
            server.send_message(message)
