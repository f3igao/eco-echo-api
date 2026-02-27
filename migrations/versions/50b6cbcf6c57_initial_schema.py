"""initial schema

Revision ID: 50b6cbcf6c57
Revises: 
Create Date: 2026-02-27 16:37:48.427643

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '50b6cbcf6c57'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('wishlist', schema=None) as batch_op:
        batch_op.add_column(sa.Column('planned_date_start', sa.Date(), nullable=True))
        batch_op.add_column(sa.Column('planned_date_end', sa.Date(), nullable=True))
        batch_op.add_column(sa.Column('notes', sa.Text(), nullable=True))


def downgrade():
    with op.batch_alter_table('wishlist', schema=None) as batch_op:
        batch_op.drop_column('notes')
        batch_op.drop_column('planned_date_end')
        batch_op.drop_column('planned_date_start')
