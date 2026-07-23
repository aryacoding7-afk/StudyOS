"""add hnsw vector index

Revision ID: f426eb805cbb
Revises: 0233b64c6487
Create Date: 2026-07-23 19:49:15.775361

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f426eb805cbb'
down_revision: Union[str, Sequence[str], None] = '0233b64c6487'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.execute("""
        CREATE INDEX document_chunks_embedding_hnsw_idx
        ON document_chunks
        USING hnsw (embedding vector_cosine_ops);
    """)


def downgrade() -> None:
    """Downgrade schema."""

    op.execute("""
        DROP INDEX document_chunks_embedding_hnsw_idx;
    """)
