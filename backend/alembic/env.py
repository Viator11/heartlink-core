import os
from alembic import context
from sqlalchemy import engine_from_config, pool
from sqlmodel import SQLModel
from app.db.session import engine
from app.models.user import User
from app.models.profile import Profile
from app.models.match import Match
from app.models.message import Message
from app.models.billing import Subscription
from app.models.moderation import Report, Block

config = context.config
target_metadata = SQLModel.metadata

def run_migrations_offline():
    url = os.getenv("DB_URL") or str(engine.url)
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    connectable = engine
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
