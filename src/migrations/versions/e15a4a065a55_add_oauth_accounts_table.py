"""add_oauth_accounts_table

Revision ID: e15a4a065a55
Revises: 39f31fe36956
Create Date: 2023-07-24 16:12:25.180566

"""
import fastapi_users_db_sqlalchemy
import sqlalchemy as sa
from alembic import op

revision = 'e15a4a065a55'
down_revision = '39f31fe36956'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'oauth_accounts',
        sa.Column('user_id', fastapi_users_db_sqlalchemy.generics.GUID(), nullable=False),
        sa.Column('id', fastapi_users_db_sqlalchemy.generics.GUID(), nullable=False),
        sa.Column('oauth_name', sa.String(length=100), nullable=False),
        sa.Column('access_token', sa.String(length=1024), nullable=False),
        sa.Column('expires_at', sa.Integer(), nullable=True),
        sa.Column('refresh_token', sa.String(length=1024), nullable=True),
        sa.Column('account_id', sa.String(length=320), nullable=False),
        sa.Column('account_email', sa.String(length=320), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='cascade'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_oauth_accounts_account_id'), 'oauth_accounts', ['account_id'], unique=False)
    op.create_index(op.f('ix_oauth_accounts_oauth_name'), 'oauth_accounts', ['oauth_name'], unique=False)
    op.alter_column(
        'users',
        'hashed_password',
        existing_type=sa.VARCHAR(length=1024),
        nullable=True
    )
    op.create_index(op.f('ix_users_hashed_password'), 'users', ['hashed_password'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_users_hashed_password'), table_name='users')
    op.alter_column(
        'users',
        'hashed_password',
        existing_type=sa.VARCHAR(length=1024),
        nullable=False
    )
    op.drop_index(op.f('ix_oauth_accounts_oauth_name'), table_name='oauth_accounts')
    op.drop_index(op.f('ix_oauth_accounts_account_id'), table_name='oauth_accounts')
    op.drop_table('oauth_accounts')
