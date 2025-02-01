"""init

Revision ID: 111c943514e6
Revises: 
Create Date: 2025-02-01 12:56:00.691910

"""
from alembic import op
import sqlalchemy as sa

from src.auth.models import TZDateTime

# revision identifiers, used by Alembic.
revision = '111c943514e6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('email', sa.String(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.Column('password', sa.String(), nullable=False),
    sa.Column('description', sa.String(length=200), nullable=True),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('account_type', sa.Enum('startup', 'tester', name='accounttype'), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('applications',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('description', sa.String(length=1000), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.Column('hide_reviews', sa.Boolean(), nullable=False),
    sa.Column('deleted', sa.Boolean(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('refresh_tokens',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('token', sa.String(), nullable=False),
    sa.Column('created_at', TZDateTime(), nullable=False),
    sa.Column('expires_at', TZDateTime(), nullable=False),
    sa.Column('revoked', sa.Boolean(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reviews',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('body', sa.String(length=1000), nullable=False),
    sa.Column('date_created', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('review_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['review_id'], ['reviews.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('ratings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('grade', sa.Enum('grade_1', 'grade_2', 'grade_3', 'grade_4', 'grade_5', name='ratinggrade'), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('review_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['review_id'], ['reviews.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('review_votes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('vote_type', sa.Boolean(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('review_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['review_id'], ['reviews.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comment_votes',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('vote_type', sa.Boolean(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('comment_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['comment_id'], ['comments.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment_votes')
    op.drop_table('review_votes')
    op.drop_table('ratings')
    op.drop_table('comments')
    op.drop_table('reviews')
    op.drop_table('refresh_tokens')
    op.drop_table('applications')
    op.drop_table('users')
    # ### end Alembic commands ###
