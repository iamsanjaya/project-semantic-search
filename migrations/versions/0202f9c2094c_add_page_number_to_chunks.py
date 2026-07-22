"""add page_number to chunks

Revision ID: 0202f9c2094c
Revises:
Create Date: 2026-07-01 15:27:41.079061

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "0202f9c2094c"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. add nullable column first
    op.add_column("chunks", sa.Column("page_number", sa.Integer(), nullable=True))

    # 2. backfill existing rows
    op.execute("UPDATE chunks SET page_number = 0")

    # 3. enforce NOT NULL constraint
    op.alter_column("chunks", "page_number", nullable=False)


def downgrade() -> None:
    op.drop_column("chunks", "page_number")
