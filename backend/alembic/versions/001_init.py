"""empty init

Revision ID: 001_init
Revises: 
Create Date: 2025-10-07
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "001_init"
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    # Пустая стартовая миграция — таблицы создаются SQLModel.metadata.create_all() на старте,
    # либо добавь автогенерацию ниже отдельной ревизией.
    pass

def downgrade():
    pass

