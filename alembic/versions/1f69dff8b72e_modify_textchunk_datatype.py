"""Modify TextChunk datatype

Revision ID: 1f69dff8b72e
Revises: 2318e7fe35ba
Create Date: 2023-10-27 12:08:02.385143

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1f69dff8b72e'
down_revision: Union[str, None] = '2318e7fe35ba'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('text_chunks', schema=None) as batch_op:
        batch_op.alter_column('chunk_content',
               existing_type=sa.VARCHAR(),
               type_=sa.Text(),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('text_chunks', schema=None) as batch_op:
        batch_op.alter_column('chunk_content',
               existing_type=sa.Text(),
               type_=sa.VARCHAR(),
               existing_nullable=True)

    # ### end Alembic commands ###
