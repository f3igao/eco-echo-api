"""add social media features

Revision ID: c3e7f1a09b52
Revises: a1f3d8e92b04
Create Date: 2026-03-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3e7f1a09b52'
down_revision = 'a1f3d8e92b04'
branch_labels = None
depends_on = None


def upgrade():
    # Add is_private to user table
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_private', sa.Boolean(), nullable=False, server_default=sa.false()))

    # Create follow table
    op.create_table(
        'follow',
        sa.Column('follow_id', sa.Integer(), nullable=False),
        sa.Column('follower_id', sa.Integer(), nullable=False),
        sa.Column('following_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['follower_id'], ['user.user_id']),
        sa.ForeignKeyConstraint(['following_id'], ['user.user_id']),
        sa.PrimaryKeyConstraint('follow_id'),
        sa.UniqueConstraint('follower_id', 'following_id', name='uq_follow'),
    )

    # Create forum_post table
    op.create_table(
        'forum_post',
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('park_id', sa.Integer(), nullable=True),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('body', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['park_id'], ['park.park_id']),
        sa.ForeignKeyConstraint(['user_id'], ['user.user_id']),
        sa.PrimaryKeyConstraint('post_id'),
    )

    # Create forum_comment table
    op.create_table(
        'forum_comment',
        sa.Column('comment_id', sa.Integer(), nullable=False),
        sa.Column('post_id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('body', sa.Text(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['post_id'], ['forum_post.post_id']),
        sa.ForeignKeyConstraint(['user_id'], ['user.user_id']),
        sa.PrimaryKeyConstraint('comment_id'),
    )


def downgrade():
    op.drop_table('forum_comment')
    op.drop_table('forum_post')
    op.drop_table('follow')

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('is_private')
