import pyotp
from ..core.config import get_settings

def generate_secret() -> str:
    return pyotp.random_base32()

def provisioning_uri(email: str, secret: str) -> str:
    return pyotp.totp.TOTP(secret).provisioning_uri(name=email, issuer_name=get_settings().TOTP_ISSUER)

def verify(secret: str, code: str) -> bool:
    return pyotp.TOTP(secret).verify(code, valid_window=1)
