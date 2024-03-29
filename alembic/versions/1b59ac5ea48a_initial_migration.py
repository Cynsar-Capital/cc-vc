"""Initial migration

Revision ID: 1b59ac5ea48a
Revises: 
Create Date: 2023-10-26 17:08:48.424183

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1b59ac5ea48a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('text_chunks',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('chunk', sa.String(), nullable=True),
    sa.Column('file_name', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('text_chunks')
    # ### end Alembic commands ###
