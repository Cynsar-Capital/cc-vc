from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '33d773c3789e'
down_revision = '5a7e4ebb81c3'
branch_labels = None
depends_on = None

def upgrade():
    # Create files table
    conn = op.get_bind()
    if not conn.dialect.has_table(conn, "files"):
        op.create_table('files',
                        sa.Column('id', sa.Integer(), nullable=False),
                        sa.Column('file_name', sa.String(), nullable=True),
                        sa.PrimaryKeyConstraint('id'),
                        sa.UniqueConstraint('file_name')
                        )
    # Using batch mode for operations on 'text_chunks' table
    with op.batch_alter_table("text_chunks") as batch_op:
        batch_op.add_column(sa.Column('chunk_content', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('file_id', sa.Integer(), nullable=True))
        batch_op.create_foreign_key("fk_text_chunks_file_id", 'files', ['file_id'], ['id'])
        batch_op.drop_column('chunk')
        batch_op.drop_column('file_name')

def downgrade():
    with op.batch_alter_table("text_chunks") as batch_op:
        batch_op.drop_column('chunk_content')
        batch_op.drop_column('file_id')
        batch_op.add_column(sa.Column('file_name', sa.VARCHAR(), nullable=True))
        batch_op.add_column(sa.Column('chunk', sa.VARCHAR(), nullable=True))

    # Drop the files table
    op.drop_table('files')
