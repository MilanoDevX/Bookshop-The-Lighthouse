"""empty message

Revision ID: a121851fc315
Revises: 391500623670
Create Date: 2025-02-26 17:48:49.203130

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a121851fc315'
down_revision = '391500623670'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Books',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=200), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('full_name',
               existing_type=sa.VARCHAR(length=260),
               type_=sa.String(length=200),
               existing_nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.alter_column('full_name',
               existing_type=sa.String(length=200),
               type_=sa.VARCHAR(length=260),
               existing_nullable=False)

    op.drop_table('Books')
    # ### end Alembic commands ###
