"""changes string literal in user's role column

Revision ID: c42fd579ecf6
Revises: 25abebca724f
Create Date: 2025-08-19 10:10:26.898019

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "c42fd579ecf6"
down_revision: Union[str, Sequence[str], None] = "25abebca724f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "users",
        "role",
        existing_type=sa.String(length=20),
        server_default=sa.text("'user'"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "users",
        "role",
        existing_type=sa.String(length=20),
        server_default=None,  # remove default on downgrade
    )
