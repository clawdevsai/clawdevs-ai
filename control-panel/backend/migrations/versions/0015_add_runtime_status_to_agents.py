"""Add runtime_status to agents table

Revision ID: 0015
Revises: 0014
Create Date: 2026-03-28 23:46:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0015'
down_revision = '0014'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'agents',
        sa.Column('runtime_status', sa.String(), nullable=False, server_default='offline')
    )
    # Update existing rows to have runtime_status computed from heartbeat
    op.execute("""
        UPDATE agents
        SET runtime_status = 'offline'
        WHERE runtime_status IS NULL OR runtime_status = ''
    """)


def downgrade() -> None:
    op.drop_column('agents', 'runtime_status')
