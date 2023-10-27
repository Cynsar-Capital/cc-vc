"""Modified DB Tables

Revision ID: 5a7e4ebb81c3
Revises: 1b59ac5ea48a
Create Date: 2023-10-26 17:30:35.979916

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5a7e4ebb81c3'
down_revision: Union[str, None] = '1b59ac5ea48a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
