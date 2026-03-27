"""add trigger_type to cron_executions

Revision ID: 0007
Revises: 0006
Create Date: 2026-03-27 10:35:00.000000
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0007"
down_revision = "0006"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        sa.text(
            """
            ALTER TABLE cron_executions
            ADD COLUMN IF NOT EXISTS trigger_type VARCHAR NOT NULL DEFAULT 'scheduled'
            """
        )
    )


def downgrade() -> None:
    op.execute(
        sa.text(
            """
            ALTER TABLE cron_executions
            DROP COLUMN IF EXISTS trigger_type
            """
        )
    )
