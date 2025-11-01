from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.email_postmark import send_verify_email
import asyncio

router = APIRouter()

# Модель данных регистрации
class RegisterRequest(BaseModel):
    email: str
    username: str

@router.post("/register")
async def register_user(request: RegisterRequest):
    # Имитация создания пользователя
    print(f"✅ New user registered: {request.email}")

    # Генерируем ссылку подтверждения
    verify_link = f"https://heartlink.love/verify?code=devtest"

    # Отправляем письмо
    asyncio.create_task(
        send_verify_email(
            email=request.email,
            username=request.username,
            verify_link=verify_link,
            lang="en"
        )
    )

    return {"message": "User registered. Verification email sent!"}
