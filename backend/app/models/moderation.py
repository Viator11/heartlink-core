from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Report(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    reporter_id: int
    target_user_id: int
    reason: str
    status: str = "open"  # open | reviewing | resolved
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Block(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int
    blocked_user_id: int
    created_at: datetime = Field(default_factory=datetime.utcnow)