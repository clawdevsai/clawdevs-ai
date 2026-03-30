"""Add chat_panel_transcripts for UI transcript cache

Revision ID: 0017
Revises: 0016
Create Date: 2026-03-30 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0017"
down_revision = "0016"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "chat_panel_transcripts",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("agent_slug", sa.String(length=64), nullable=False),
        sa.Column("session_key", sa.String(length=512), nullable=False),
        sa.Column("messages", sa.JSON(), nullable=False),
        sa.Column("last_turn_id", sa.String(length=96), nullable=True),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "agent_slug",
            "session_key",
            name="uq_chat_panel_transcripts_agent_session_key",
        ),
    )
    op.create_index(
        "ix_chat_panel_transcripts_agent_slug",
        "chat_panel_transcripts",
        ["agent_slug"],
        unique=False,
    )


def downgrade() -> None:
    op.drop_index("ix_chat_panel_transcripts_agent_slug", table_name="chat_panel_transcripts")
    op.drop_table("chat_panel_transcripts")
