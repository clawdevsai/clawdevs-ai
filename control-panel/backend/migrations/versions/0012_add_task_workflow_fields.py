"""add task workflow orchestration fields

Revision ID: 0012
Revises: 0011
Create Date: 2026-03-28
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0012"
down_revision = "0011"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("tasks") as batch_op:
        batch_op.add_column(
            sa.Column(
                "workflow_state",
                sa.String(),
                nullable=False,
                server_default="queued_to_ceo",
            )
        )
        batch_op.add_column(sa.Column("workflow_last_error", sa.String(), nullable=True))
        batch_op.add_column(
            sa.Column(
                "workflow_attempts",
                sa.Integer(),
                nullable=False,
                server_default="0",
            )
        )
        batch_op.create_index(
            "ix_tasks_workflow_state",
            ["workflow_state"],
            unique=False,
        )


def downgrade() -> None:
    with op.batch_alter_table("tasks") as batch_op:
        batch_op.drop_index("ix_tasks_workflow_state")
        batch_op.drop_column("workflow_attempts")
        batch_op.drop_column("workflow_last_error")
        batch_op.drop_column("workflow_state")
