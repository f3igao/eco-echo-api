"""remove activities, add activities text to park_review

Revision ID: a1f3d8e92b04
Revises: 50b6cbcf6c57
Create Date: 2026-02-27 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1f3d8e92b04'
down_revision = '50b6cbcf6c57'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('park_review', schema=None) as batch_op:
        batch_op.add_column(sa.Column('activities', sa.Text(), nullable=True))

    op.drop_table('user_activity_tag')
    op.drop_table('user_activity_review')
    op.drop_table('activity_review')
    op.drop_table('activity')


def downgrade():
    op.create_table(
        'activity',
        sa.Column('activity_id', sa.Integer(), nullable=False),
        sa.Column('park_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('duration', sa.Integer(), nullable=False),
        sa.Column('difficulty', sa.Float(precision=2), nullable=False),
        sa.Column('require_special_equipment', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['park_id'], ['park.park_id']),
        sa.PrimaryKeyConstraint('activity_id'),
    )
    op.create_table(
        'activity_review',
        sa.Column('activity_review_id', sa.Integer(), nullable=False),
        sa.Column('activity_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('rating', sa.Float(), nullable=False),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.Column('media_url', sa.String(length=255), nullable=True),
        sa.Column('is_private', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['activity_id'], ['activity.activity_id']),
        sa.ForeignKeyConstraint(['user_id'], ['user.user_id']),
        sa.PrimaryKeyConstraint('activity_review_id'),
    )
    op.create_table(
        'user_activity_review',
        sa.Column('user_activity_review_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('activity_review_id', sa.Integer(), nullable=False),
        sa.Column('rating', sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(['activity_review_id'], ['activity_review.activity_review_id']),
        sa.ForeignKeyConstraint(['user_id'], ['user.user_id']),
        sa.PrimaryKeyConstraint('user_activity_review_id'),
    )
    op.create_table(
        'user_activity_tag',
        sa.Column('user_activity_tag_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('activity_review_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['activity_review_id'], ['activity_review.activity_review_id']),
        sa.ForeignKeyConstraint(['user_id'], ['user.user_id']),
        sa.PrimaryKeyConstraint('user_activity_tag_id'),
    )

    with op.batch_alter_table('park_review', schema=None) as batch_op:
        batch_op.drop_column('activities')
