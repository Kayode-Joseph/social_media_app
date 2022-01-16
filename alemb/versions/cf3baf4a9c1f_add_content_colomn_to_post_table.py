"""add content colomn to post table

Revision ID: cf3baf4a9c1f
Revises: 6eb85334ae73
Create Date: 2022-01-15 11:36:57.551258

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cf3baf4a9c1f'
down_revision = '6eb85334ae73'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
