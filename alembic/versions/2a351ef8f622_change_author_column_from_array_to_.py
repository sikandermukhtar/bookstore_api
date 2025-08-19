"""Change author column from array to string

Revision ID: 2a351ef8f622
Revises: b88169abd2e5
Create Date: 2025-08-19 11:29:54.509651

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "2a351ef8f622"
down_revision: Union[str, Sequence[str], None] = "b88169abd2e5"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
