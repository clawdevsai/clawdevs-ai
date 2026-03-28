"""add memory embedding metadata columns

Revision ID: 0011
Revises: 0010
Create Date: 2026-03-28
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0011"
down_revision = "0010"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with op.batch_alter_table("memory_entries") as batch_op:
        batch_op.add_column(
            sa.Column(
                "embedding_model",
                sa.String(),
                nullable=False,
                server_default="mistral",
            )
        )
        batch_op.add_column(
            sa.Column(
                "chunk_index",
                sa.Integer(),
                nullable=False,
                server_default="0",
            )
        )
        batch_op.add_column(
            sa.Column("source_file_path", sa.String(), nullable=True)
        )
        batch_op.add_column(
            sa.Column("embedding_generated_at", sa.DateTime(), nullable=True)
        )


def downgrade() -> None:
    with op.batch_alter_table("memory_entries") as batch_op:
        batch_op.drop_column("embedding_generated_at")
        batch_op.drop_column("source_file_path")
        batch_op.drop_column("chunk_index")
        batch_op.drop_column("embedding_model")
