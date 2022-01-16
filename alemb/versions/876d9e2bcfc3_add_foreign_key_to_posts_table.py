"""add foreign key to posts table

Revision ID: 876d9e2bcfc3
Revises: df895ae2128e
Create Date: 2022-01-15 12:59:50.587091

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '876d9e2bcfc3'
down_revision = 'df895ae2128e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id',sa.Integer(),nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users",local_cols=['owner_id'], remote_cols=['id'], ondelete= "CASCADE")
    pass


def downgrade():
    op.drop_constaint('post_users_fk', table_name= "posts")
    op.drop_column('posts','owner_id')
    pass
