import hashlib, secrets
from datetime import datetime, timedelta
from jose import jwt
from .config import get_settings

def _jti(): return hashlib.sha256(secrets.token_bytes(32)).hexdigest()

def create_access_token(sub, extra=None, jti=None):
    s = get_settings()
    now = datetime.utcnow()
    jti = jti or _jti()
    payload = {"sub": sub, "iat": int(now.timestamp()),
               "exp": int((now + timedelta(minutes=s.ACCESS_TTL_MIN)).timestamp()),
               "jti": jti}
    if extra: payload.update(extra)
    token = jwt.encode(payload, s.JWT_SECRET, algorithm="HS256")
    return {"token": token, "exp": payload["exp"], "jti": jti}

def create_refresh_token(sub, extra=None):
    s = get_settings()
    now = datetime.utcnow()
    jti = _jti()
    payload = {"sub": sub, "iat": int(now.timestamp()),
               "exp": int((now + timedelta(days=s.REFRESH_TTL_DAYS)).timestamp()),
               "jti": jti, "type": "refresh"}
    if extra: payload.update(extra)
    token = jwt.encode(payload, s.JWT_SECRET, algorithm="HS256")
    return {"token": token, "exp": payload["exp"], "jti": jti}

def verify_token(token:str):
    return jwt.decode(token, get_settings().JWT_SECRET, algorithms=["HS256"])