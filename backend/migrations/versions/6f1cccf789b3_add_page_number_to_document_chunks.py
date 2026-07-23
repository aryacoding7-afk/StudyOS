"""add page number to document chunks

Revision ID: 6f1cccf789b3
Revises: f426eb805cbb
Create Date: 2026-07-23 20:51:28.814850

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6f1cccf789b3'
down_revision: Union[str, Sequence[str], None] = 'f426eb805cbb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "document_chunks",
        sa.Column(
            "page_number",
            sa.Integer(),
            nullable=False,
            server_default="1",
        ),
    )

    op.alter_column(
        "document_chunks",
        "page_number",
        server_default=None,
    )


def downgrade() -> None:
    op.drop_column(
        "document_chunks",
        "page_number",
    )