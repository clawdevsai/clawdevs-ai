"""align activity_events schema with model

Revision ID: 0013
Revises: 0012
Create Date: 2026-03-28
"""

from alembic import op


# revision identifiers, used by Alembic.
revision = "0013"
down_revision = "0012"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute("ALTER TABLE activity_events ADD COLUMN IF NOT EXISTS user_id uuid")
    op.execute(
        "ALTER TABLE activity_events ADD COLUMN IF NOT EXISTS entity_type varchar"
    )
    op.execute("ALTER TABLE activity_events ADD COLUMN IF NOT EXISTS entity_id varchar")


def downgrade() -> None:
    op.execute("ALTER TABLE activity_events DROP COLUMN IF EXISTS entity_id")
    op.execute("ALTER TABLE activity_events DROP COLUMN IF EXISTS entity_type")
    op.execute("ALTER TABLE activity_events DROP COLUMN IF EXISTS user_id")
