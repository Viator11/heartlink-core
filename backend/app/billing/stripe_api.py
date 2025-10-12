from fastapi import APIRouter, Header, HTTPException
from ..core.config import get_settings
from ..core.security import verify_token

router = APIRouter(prefix="/billing", tags=["billing"])
s = get_settings()

@router.post("/subscribe")
def subscribe(plan: str, authorization: str = Header(...)):
    # Заглушка Stripe — добавь реальную интеграцию при готовности ключей
    if not s.STRIPE_SECRET_KEY:
        raise HTTPException(503, "Stripe not configured")
    _ = verify_token(authorization.split()[1])  # validate user
    return {"checkout_url": "https://example.com/stripe/checkout?plan="+plan}