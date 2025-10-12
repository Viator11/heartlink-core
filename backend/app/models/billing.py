from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Subscription(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, foreign_key="user.id")
    plan: str = "free"          # 'free' | 'pro' | 'boost'
    active: bool = False
    stripe_customer_id: Optional[str] = None
    stripe_sub_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)