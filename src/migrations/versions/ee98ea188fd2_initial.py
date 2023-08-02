"""initial

Revision ID: ee98ea188fd2
Revises:
Create Date: 2023-08-01 19:43:35.912670

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'ee98ea188fd2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'events',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=True),
        sa.Column('summary', sa.String(length=1000), nullable=True),
        sa.Column('image_url', sa.String(length=255), nullable=True),
        sa.Column('source', sa.String(length=100), nullable=True),
        sa.Column('source_id', sa.String(length=100), nullable=True),
        sa.Column('online_event', sa.Boolean(), server_default='False', nullable=False),
        sa.Column('start', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('end', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=45), nullable=True),
        sa.Column('hashed_password', sa.String(length=1024), nullable=True),
        sa.Column('verified', sa.Boolean(), server_default='False', nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
                  nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'),
                  nullable=False),
        sa.Column('avatar_path', sa.String(length=255), nullable=True),
        sa.Column('tfa_secret', sa.String(length=32), nullable=True),
        sa.Column('tfa_enabled', sa.Boolean(), server_default='False', nullable=False),
        sa.Column('is_superuser', sa.Boolean(), nullable=False),
        sa.Column('is_moderator', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_hashed_password'), 'users', ['hashed_password'], unique=True)
    op.create_index(op.f('ix_users_tfa_secret'), 'users', ['tfa_secret'], unique=True)
    op.create_table(
        'oauth_accounts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('oauth_name', sa.String(length=100), nullable=False),
        sa.Column('access_token', sa.String(length=1024), nullable=False),
        sa.Column('expires_at', sa.Integer(), nullable=True),
        sa.Column('refresh_token', sa.String(length=1024), nullable=True),
        sa.Column('account_id', sa.String(length=320), nullable=False),
        sa.Column('account_email', sa.String(length=320), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='cascade'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_oauth_accounts_account_id'), 'oauth_accounts', ['account_id'], unique=False)
    op.create_index(op.f('ix_oauth_accounts_oauth_name'), 'oauth_accounts', ['oauth_name'], unique=False)
    op.create_table(
        'users_events',
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('event_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['event_id'], ['events.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('user_id', 'event_id')
    )


def downgrade() -> None:
    op.drop_table('users_events')
    op.drop_index(op.f('ix_oauth_accounts_oauth_name'), table_name='oauth_accounts')
    op.drop_index(op.f('ix_oauth_accounts_account_id'), table_name='oauth_accounts')
    op.drop_table('oauth_accounts')
    op.drop_index(op.f('ix_users_tfa_secret'), table_name='users')
    op.drop_index(op.f('ix_users_hashed_password'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_table('events')
