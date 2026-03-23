"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-03-22 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects.postgresql import JSONB

# revision identifiers, used by Alembic.
revision: str = "0001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Users table
    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("password_hash", sa.String(), nullable=False),
        sa.Column("role", sa.String(), nullable=False, server_default="viewer"),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_users_username", "users", ["username"], unique=True)

    # Agents table
    op.create_table(
        "agents",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("slug", sa.String(), nullable=False),
        sa.Column("display_name", sa.String(), nullable=False),
        sa.Column("role", sa.String(), nullable=False),
        sa.Column("avatar_url", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=False, server_default="unknown"),
        sa.Column("current_model", sa.String(), nullable=True),
        sa.Column("openclaw_session_id", sa.String(), nullable=True),
        sa.Column("last_heartbeat_at", sa.DateTime(), nullable=True),
        sa.Column("cron_expression", sa.String(), nullable=True),
        sa.Column("cron_last_run_at", sa.DateTime(), nullable=True),
        sa.Column("cron_next_run_at", sa.DateTime(), nullable=True),
        sa.Column("cron_status", sa.String(), nullable=False, server_default="idle"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_agents_slug", "agents", ["slug"], unique=True)

    # Approvals table
    op.create_table(
        "approvals",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("agent_id", sa.UUID(), nullable=True),
        sa.Column("openclaw_approval_id", sa.String(), nullable=True),
        sa.Column("action_type", sa.String(), nullable=False),
        sa.Column("payload", JSONB(), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("rubric_scores", JSONB(), nullable=True),
        sa.Column("status", sa.String(), nullable=False, server_default="pending"),
        sa.Column("decided_by_id", sa.UUID(), nullable=True),
        sa.Column("justification", sa.String(), nullable=True),
        sa.Column("decided_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["agent_id"], ["agents.id"]),
        sa.ForeignKeyConstraint(["decided_by_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_approvals_openclaw_approval_id", "approvals", ["openclaw_approval_id"])

    # Sessions table
    op.create_table(
        "sessions",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("agent_id", sa.UUID(), nullable=True),
        sa.Column("openclaw_session_id", sa.String(), nullable=False),
        sa.Column("channel", sa.String(), nullable=True),
        sa.Column("peer", sa.String(), nullable=True),
        sa.Column("message_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("token_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("status", sa.String(), nullable=False, server_default="active"),
        sa.Column("started_at", sa.DateTime(), nullable=False),
        sa.Column("ended_at", sa.DateTime(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["agent_id"], ["agents.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_sessions_openclaw_session_id", "sessions", ["openclaw_session_id"], unique=True)
    op.create_index("ix_sessions_agent_id", "sessions", ["agent_id"])

    # Tasks table
    op.create_table(
        "tasks",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=False, server_default="inbox"),
        sa.Column("priority", sa.String(), nullable=False, server_default="medium"),
        sa.Column("agent_id", sa.UUID(), nullable=True),
        sa.Column("github_issue_number", sa.Integer(), nullable=True),
        sa.Column("github_issue_url", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["agent_id"], ["agents.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # SDD Artifacts table
    op.create_table(
        "sdd_artifacts",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("current_step", sa.String(), nullable=False, server_default="brief"),
        sa.Column("agent_id", sa.UUID(), nullable=True),
        sa.Column("brief", sa.Text(), nullable=True),
        sa.Column("clarify", sa.Text(), nullable=True),
        sa.Column("spec", sa.Text(), nullable=True),
        sa.Column("plan", sa.Text(), nullable=True),
        sa.Column("task_doc", sa.Text(), nullable=True),
        sa.Column("validate_doc", sa.Text(), nullable=True),
        sa.Column("github_issue_number", sa.Integer(), nullable=True),
        sa.Column("github_issue_url", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["agent_id"], ["agents.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # Memory entries table
    op.create_table(
        "memory_entries",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("agent_id", sa.UUID(), nullable=True),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("tags", JSONB(), nullable=True),
        sa.Column("is_active", sa.Boolean(), nullable=False, server_default="true"),
        sa.Column("is_candidate", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("file_path", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["agent_id"], ["agents.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # Cron executions table
    op.create_table(
        "cron_executions",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("agent_id", sa.UUID(), nullable=True),
        sa.Column("cron_name", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("started_at", sa.DateTime(), nullable=False),
        sa.Column("completed_at", sa.DateTime(), nullable=True),
        sa.Column("duration_ms", sa.Integer(), nullable=True),
        sa.Column("log_output", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["agent_id"], ["agents.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # Activity events table
    op.create_table(
        "activity_events",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("agent_id", sa.UUID(), nullable=True),
        sa.Column("user_id", sa.UUID(), nullable=True),
        sa.Column("event_type", sa.String(), nullable=False),
        sa.Column("payload", JSONB(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["agent_id"], ["agents.id"]),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )

    # Metrics table
    op.create_table(
        "metrics",
        sa.Column("id", sa.UUID(), nullable=False),
        sa.Column("agent_id", sa.UUID(), nullable=True),
        sa.Column("period", sa.String(), nullable=False),
        sa.Column("token_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("task_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("approval_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("error_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("recorded_at", sa.DateTime(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["agent_id"], ["agents.id"]),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("metrics")
    op.drop_table("activity_events")
    op.drop_table("cron_executions")
    op.drop_table("memory_entries")
    op.drop_table("sdd_artifacts")
    op.drop_table("tasks")
    op.drop_table("sessions")
    op.drop_table("approvals")
    op.drop_table("agents")
    op.drop_table("users")
