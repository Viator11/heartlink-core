revision = "xxxx_add_security_logs"
down_revision = None
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa

def upgrade():
    op.create_table(
        "security_logs",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="SET NULL"), nullable=True),
        sa.Column("action", sa.String(48), nullable=False),
        sa.Column("ip", sa.String(64)),
        sa.Column("user_agent", sa.Text()),
        sa.Column("created_at", sa.DateTime, nullable=False),
    )
    op.create_index("ix_security_logs_user_id", "security_logs", ["user_id"])
    op.create_index("ix_security_logs_created_at", "security_logs", ["created_at"])
    op.create_index("ix_security_logs_action", "security_logs", ["action"])

def downgrade():
    op.drop_index("ix_security_logs_action", table_name="security_logs")
    op.drop_index("ix_security_logs_created_at", table_name="security_logs")
    op.drop_index("ix_security_logs_user_id", table_name="security_logs")
    op.drop_table("security_logs")
