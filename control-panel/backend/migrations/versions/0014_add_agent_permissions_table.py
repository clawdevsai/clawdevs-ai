"""Add agent_permissions table

Revision ID: 0014
Revises: 0013
Create Date: 2026-03-28 23:45:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql
from uuid import uuid4

# revision identifiers, used by Alembic.
revision = '0014'
down_revision = '0013'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create agent_permissions table
    op.create_table(
        'agent_permissions',
        sa.Column('id', postgresql.UUID(as_uuid=True), nullable=False, default=uuid4),
        sa.Column('agent_slug', sa.String(), nullable=False, index=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=False, index=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    )


def downgrade() -> None:
    op.drop_table('agent_permissions')
