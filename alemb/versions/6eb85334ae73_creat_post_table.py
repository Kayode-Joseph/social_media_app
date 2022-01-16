"""creat post table

Revision ID: 6eb85334ae73
Revises: 0fa0ad86be13
Create Date: 2022-01-15 11:00:24.409063

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6eb85334ae73'
down_revision = '0fa0ad86be13'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
   sa.Column('title', sa.String(), nullable=False ) )
    pass


def downgrade():
    op.drop_table('posts')
    pass
