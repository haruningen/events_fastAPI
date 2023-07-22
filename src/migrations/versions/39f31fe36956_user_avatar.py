"""

Revision ID: 39f31fe36956
Revises: 923f7e042486
Create Date: 2023-07-21 09:04:48.245771

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '39f31fe36956'
down_revision = '923f7e042486'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('users', sa.Column('avatar_path', sa.String(length=255), nullable=True))
    op.drop_column('users', 'avatar_url')


def downgrade() -> None:
    op.add_column('users', sa.Column('avatar_url', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('users', 'avatar_path')
