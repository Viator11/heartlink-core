from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, EmailStr
from datetime import datetime, timedelta
import secrets

router = APIRouter(prefix="/auth", tags=["auth"])

def get_db():
    raise NotImplementedError

def get_current_user():
    raise NotImplementedError

TOKENS = {}

class RegisterIn(BaseModel):
    email: EmailStr
    password: str
    username: str | None = None
    lang: str | None = None

class ResendIn(BaseModel):
    email: EmailStr
    lang: str | None = None

@router.post("/register")
def register(payload: RegisterIn, request: Request):
    token = secrets.token_urlsafe(32)
    TOKENS[token] = {
        "email": payload.email,
        "exp": datetime.utcnow() + timedelta(hours=24),
        "lang": (payload.lang or request.headers.get("Accept-Language", "ru"))[:2]
    }
    scheme = request.headers.get("X-Forwarded-Proto") or request.url.scheme
    host = request.headers.get("X-Forwarded-Host") or request.url.netloc
    verify_link = f"{scheme}://{host}/auth/verify?token={token}"
    # send_verify_email(email=payload.email, username=payload.username, verify_link=verify_link, lang=TOKENS[token]["lang"])
    return {"ok": True, "action": "verification_sent"}

@router.get("/verify")
def verify(token: str):
    item = TOKENS.get(token)
    if not item or item["exp"] < datetime.utcnow():
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    TOKENS.pop(token, None)
    return {"ok": True, "verified": True}

@router.post("/resend-email")
def resend(payload: ResendIn, request: Request):
    token = secrets.token_urlsafe(32)
    TOKENS[token] = {
        "email": payload.email,
        "exp": datetime.utcnow() + timedelta(hours=24),
        "lang": (payload.lang or request.headers.get("Accept-Language", "ru"))[:2]
    }
    scheme = request.headers.get("X-Forwarded-Proto") or request.url.scheme
    host = request.headers.get("X-Forwarded-Host") or request.url.netloc
    verify_link = f"{scheme}://{host}/auth/verify?token={token}"
    # send_verify_email(email=payload.email, username=None, verify_link=verify_link, lang=TOKENS[token]["lang"])
    return {"ok": True, "action": "verification_resent"}
