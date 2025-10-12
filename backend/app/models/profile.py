from sqlmodel import SQLModel, Field
from datetime import datetime, date
from typing import Optional

class Profile(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True, foreign_key="user.id")
    display_name: Optional[str] = None
    bio: Optional[str] = None
    gender: Optional[str] = None
    birthday: Optional[date] = None
    city: Optional[str] = None
    country: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    interests: Optional[str] = None   # comma-separated
    photos: Optional[str] = None       # JSON array of S3 keys
    created_at: datetime = Field(default_factory=datetime.utcnow)