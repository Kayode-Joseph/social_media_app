"""add user table

Revision ID: df895ae2128e
Revises: cf3baf4a9c1f
Create Date: 2022-01-15 12:13:18.690410

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'df895ae2128e'
down_revision = 'cf3baf4a9c1f'
branch_labels = None
depends_on = None


def upgrade():

    op.create_table('users',
    sa.Column('id',sa.Integer(),nullable=False),
    sa.Column('email',sa.String(),nullable=False),
    sa.Column('password',sa.String(),nullable=False),
    sa.Column('created_at',sa.TIMESTAMP(timezone=True),nullable=False,server_default=sa.text('now()')),

    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')




    )



    
    pass


def downgrade():
    op.drop_table('users')
    pass
