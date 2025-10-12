import smtplib
from email.message import EmailMessage
from ..core.config import get_settings

def send_email(to: str, subject: str, html: str):
    s = get_settings()
    msg = EmailMessage()
    msg["From"] = s.SMTP_FROM
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(html, subtype="html")
    with smtplib.SMTP(s.SMTP_HOST, s.SMTP_PORT) as smtp:
        # для реального SMTP добавь starttls/login при необходимости
        if s.SMTP_HOST not in ("mailhog", "localhost") and s.SMTP_PORT in (587, 465):
            try:
                smtp.starttls()
            except Exception:
                pass
        # логин опционально — зависит от провайдера
        # smtp.login(s.SMTP_USER, s.SMTP_PASSWORD)
        smtp.send_message(msg)