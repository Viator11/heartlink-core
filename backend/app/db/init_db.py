from sqlmodel import SQLModel
from .session import engine
# убедимся, что модели импортированы, чтобы попали в metadata
from ..models.user import User  # noqa: F401
from ..models.profile import Profile  # noqa: F401
from ..models.match import Match  # noqa: F401
from ..models.message import Message  # noqa: F401
from ..models.billing import Subscription  # noqa: F401
from ..models.moderation import Report, Block  # noqa: F401

def init_db():
    SQLModel.metadata.create_all(engine)