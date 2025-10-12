from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Body, Header
from sqlmodel import Session, select
from passlib.hash import bcrypt
import redis.asyncio as redis
from ..db.session import get_session
from ..models.user import User
from ..core.config import get_settings
from ..core.security import create_access_token, create_refresh_token, verify_token
from .totp import generate_secret, verify as totp_verify, provisioning_uri
from .email import send_verify_email, send_reset_email

router = APIRouter(prefix="/auth", tags=["auth"])
s = get_settings()
r = redis.from_url(s.REDIS_URL)

def _exists(session: Session, email: str) -> bool:
    return session.exec(select(User).where(User.email == email)).first() is not None

@router.post("/register")
def register(email: str = Body(...), password: str = Body(...), session: Session = Depends(get_session)):
    if len(password) < s.PASSWORD_MIN_LEN:
        raise HTTPException(400, "Password too short")
    if _exists(session, email):
        raise HTTPException(400, "Email already registered")
    user = User(email=email, hashed_password=bcrypt.hash(password))
    session.add(user); session.commit(); session.refresh(user)
    tok = create_access_token(str(user.id), {"purpose":"verify-email"})
    link = f"https://{s.DOMAIN}/api/auth/verify?token={tok['token']}"
    send_verify_email(email, link)
    return {"ok": True}

@router.get("/verify")
def verify(token: str, session: Session = Depends(get_session)):
    data = verify_token(token)
    if data.get("purpose") != "verify-email":
        raise HTTPException(400, "Invalid token")
    user = session.get(User, int(data["sub"]))
    if not user: raise HTTPException(404, "User not found")
    user.email_verified = True; session.add(user); session.commit()
    return {"ok": True}

@router.post("/login")
def login(email: str = Body(...), password: str = Body(...), code: Optional[str] = Body(None), session: Session = Depends(get_session)):
    u = session.exec(select(User).where(User.email == email)).first()
    if not u or not bcrypt.verify(password, u.hashed_password):
        raise HTTPException(401, "Invalid credentials")
    if u.totp_secret:
        if not code or not totp_verify(u.totp_secret, code):
            raise HTTPException(401, "TOTP required")
    access = create_access_token(str(u.id))
    refresh = create_refresh_token(str(u.id))
    u.last_login_at = datetime.utcnow(); session.add(u); session.commit()
    return {"access": access["token"], "refresh": refresh["token"]}

@router.post("/enable-2fa")
def enable_2fa(authorization: Optional[str] = Header(None), session: Session = Depends(get_session)):
    data = verify_token(authorization.split()[1]) if authorization else None
    uid = int(data["sub"]) if data else None
    u = session.get(User, uid)
    if not u: raise HTTPException(401, "Unauthorized")
    if u.totp_secret: return {"enabled": True}
    secret = generate_secret()
    u.totp_secret = secret; session.add(u); session.commit()
    return {"otpauth_url": provisioning_uri(u.email, secret)}

@router.post("/disable-2fa")
def disable_2fa(authorization: Optional[str] = Header(None), session: Session = Depends(get_session)):
    data = verify_token(authorization.split()[1]) if authorization else None
    uid = int(data["sub"]) if data else None
    u = session.get(User, uid)
    if not u: raise HTTPException(401, "Unauthorized")
    u.totp_secret = None; session.add(u); session.commit()
    return {"enabled": False}