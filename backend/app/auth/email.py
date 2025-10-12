from ..notifications.mailer import send_email

def send_verify_email(to: str, link: str):
    send_email(to, "Verify your email", f"<p>Confirm your account: <a href='{link}'>{link}</a></p>")

def send_reset_email(to: str, link: str):
    send_email(to, "Password reset", f"<p>Reset your password: <a href='{link}'>{link}</a></p>")