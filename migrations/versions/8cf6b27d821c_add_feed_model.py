"""Add feed model

Revision ID: 8cf6b27d821c
Revises: ea541d70b125
Create Date: 2024-02-17 15:10:49.401064

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8cf6b27d821c'
down_revision: Union[str, None] = 'ea541d70b125'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('feed',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_feed_id'), 'feed', ['id'], unique=False)
    op.create_table('users_news_feed',
    sa.Column('feed_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.Column('read', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['feed_id'], ['feed.id'], ),
    sa.ForeignKeyConstraint(['post_id'], ['post.id'], ),
    sa.PrimaryKeyConstraint('feed_id', 'post_id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users_news_feed')
    op.drop_index(op.f('ix_feed_id'), table_name='feed')
    op.drop_table('feed')
    # ### end Alembic commands ###
