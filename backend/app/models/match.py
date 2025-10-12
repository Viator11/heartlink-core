from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Match(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user1_id: int
    user2_id: int
    created_at: datetime = Field(default_factory=datetime.utcnow)