from sqlmodel import create_engine, Session
from ..core.config import get_settings

_engine = create_engine(get_settings().DB_URL, pool_pre_ping=True)

def get_session():
    with Session(_engine) as session:
        yield session

# экспортируем engine для Alembic
engine = _engine

