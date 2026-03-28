"""failure and escalation schema alignment

Revision ID: 0010
Revises: 0009
Create Date: 2026-03-27
"""

from alembic import op

revision = "0010"
down_revision = "0009"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.execute(
        """
        ALTER TABLE tasks
        ADD COLUMN IF NOT EXISTS failure_count INTEGER NOT NULL DEFAULT 0,
        ADD COLUMN IF NOT EXISTS consecutive_failures INTEGER NOT NULL DEFAULT 0,
        ADD COLUMN IF NOT EXISTS last_error VARCHAR,
        ADD COLUMN IF NOT EXISTS error_reason VARCHAR,
        ADD COLUMN IF NOT EXISTS last_failed_at TIMESTAMP WITH TIME ZONE,
        ADD COLUMN IF NOT EXISTS escalated_to_agent_id UUID,
        ADD COLUMN IF NOT EXISTS escalation_reason VARCHAR,
        ADD COLUMN IF NOT EXISTS escalated_at TIMESTAMP WITH TIME ZONE,
        ADD COLUMN IF NOT EXISTS estimated_cost DOUBLE PRECISION,
        ADD COLUMN IF NOT EXISTS actual_cost DOUBLE PRECISION NOT NULL DEFAULT 0.0,
        ADD COLUMN IF NOT EXISTS cost_tier VARCHAR
        """
    )

    op.execute(
        """
        ALTER TABLE agents
        ADD COLUMN IF NOT EXISTS can_escalate BOOLEAN NOT NULL DEFAULT FALSE,
        ADD COLUMN IF NOT EXISTS max_escalations INTEGER NOT NULL DEFAULT 0,
        ADD COLUMN IF NOT EXISTS escalations_handled INTEGER NOT NULL DEFAULT 0
        """
    )

    op.execute(
        """
        CREATE INDEX IF NOT EXISTS ix_tasks_failure_count
        ON tasks (failure_count)
        """
    )
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS ix_tasks_escalated_to_agent_id
        ON tasks (escalated_to_agent_id)
        """
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_tasks_escalated_to_agent_id")
    op.execute("DROP INDEX IF EXISTS ix_tasks_failure_count")

    op.execute("ALTER TABLE agents DROP COLUMN IF EXISTS escalations_handled")
    op.execute("ALTER TABLE agents DROP COLUMN IF EXISTS max_escalations")
    op.execute("ALTER TABLE agents DROP COLUMN IF EXISTS can_escalate")

    op.execute("ALTER TABLE tasks DROP COLUMN IF EXISTS cost_tier")
    op.execute("ALTER TABLE tasks DROP COLUMN IF EXISTS actual_cost")
    op.execute("ALTER TABLE tasks DROP COLUMN IF EXISTS estimated_cost")
    op.execute("ALTER TABLE tasks DROP COLUMN IF EXISTS escalated_at")
    op.execute("ALTER TABLE tasks DROP COLUMN IF EXISTS escalation_reason")
    op.execute("ALTER TABLE tasks DROP COLUMN IF EXISTS escalated_to_agent_id")
    op.execute("ALTER TABLE tasks DROP COLUMN IF EXISTS last_failed_at")
    op.execute("ALTER TABLE tasks DROP COLUMN IF EXISTS error_reason")
    op.execute("ALTER TABLE tasks DROP COLUMN IF EXISTS last_error")
    op.execute("ALTER TABLE tasks DROP COLUMN IF EXISTS consecutive_failures")
    op.execute("ALTER TABLE tasks DROP COLUMN IF EXISTS failure_count")
