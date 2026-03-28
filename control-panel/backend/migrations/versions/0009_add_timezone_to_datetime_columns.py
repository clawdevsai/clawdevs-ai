"""add timezone to datetime columns

Revision ID: 0009
Revises: 0008
Create Date: 2026-03-27 00:00:00.000000

"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "0009"
down_revision: Union[str, None] = "0008"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Tables and their datetime columns that need timezone
tables_with_datetime_columns = {
    "users": ["created_at"],
    "agents": ["last_heartbeat_at", "cron_last_run_at", "cron_next_run_at", "created_at", "updated_at"],
    "sessions": ["started_at", "ended_at", "last_active_at", "created_at"],
    "approvals": ["created_at", "decided_at"],
    "tasks": ["created_at", "updated_at", "due_at"],
    "sdd_artifacts": ["created_at", "updated_at"],
    "memory_entries": ["created_at", "updated_at"],
    "cron_executions": ["started_at", "finished_at"],
    "activity_events": ["created_at"],
    "metrics": ["period_start", "period_end", "created_at"],
}


def upgrade() -> None:
    """Convert all DateTime columns to DateTime with timezone."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    for table_name, columns in tables_with_datetime_columns.items():
        existing_columns = {c["name"] for c in inspector.get_columns(table_name)}
        for column_name in columns:
            if column_name not in existing_columns:
                continue
            # Alter column to add timezone
            op.alter_column(
                table_name,
                column_name,
                existing_type=sa.DateTime(),
                type_=sa.DateTime(timezone=True),
                existing_nullable=True if column_name not in [
                    "created_at", "updated_at", "started_at", "period_start"
                ] else False,
            )


def downgrade() -> None:
    """Revert all DateTime columns to without timezone."""
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    for table_name, columns in tables_with_datetime_columns.items():
        existing_columns = {c["name"] for c in inspector.get_columns(table_name)}
        for column_name in columns:
            if column_name not in existing_columns:
                continue
            op.alter_column(
                table_name,
                column_name,
                existing_type=sa.DateTime(timezone=True),
                type_=sa.DateTime(),
                existing_nullable=True if column_name not in [
                    "created_at", "updated_at", "started_at", "period_start"
                ] else False,
            )
