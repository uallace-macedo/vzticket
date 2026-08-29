"""initial schema

Revision ID: 0001
Revises:
Create Date: 2026-08-28 00:00:00.000000

"""
from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = '0001'
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column(
            'role',
            sa.Enum('CLIENT', 'ORGANIZER', 'GATEKEEPER', name='user_role'),
            nullable=False,
        ),
        sa.Column(
            'balance', sa.Numeric(10, 2), server_default='0.00', nullable=False
        ),
        sa.Column(
            'pending_balance',
            sa.Numeric(10, 2),
            server_default='0.00',
            nullable=False,
        ),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint('balance >= 0.00', name='ck_users_balance_positive'),
        sa.CheckConstraint(
            'pending_balance >= 0.00', name='ck_users_pending_balance_positive'
        ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    op.create_table(
        'events',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('organizer_id', sa.Uuid(), nullable=False),
        sa.Column('title', sa.String(length=150), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column(
            'status',
            sa.Enum(
                'PENDING_FEE', 'ACTIVE', 'CANCELLED', 'FINISHED',
                name='event_status',
            ),
            nullable=False,
        ),
        sa.Column('available_tickets', sa.Integer(), nullable=False),
        sa.Column('ticket_price', sa.Numeric(10, 2), nullable=False),
        sa.Column('service_fee', sa.Numeric(10, 2), nullable=False),
        sa.Column('ticket_title', sa.String(length=100), nullable=False),
        sa.Column('ticket_description', sa.Text(), nullable=True),
        sa.Column('event_date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('sales_start_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('sales_end_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('location_name', sa.String(length=150), nullable=False),
        sa.Column('cep', sa.String(length=8), nullable=False),
        sa.Column('address', sa.String(length=255), nullable=False),
        sa.Column('number', sa.String(length=20), nullable=False),
        sa.Column('neighborhood', sa.String(length=100), nullable=False),
        sa.Column('city', sa.String(length=100), nullable=False),
        sa.Column('city_slug', sa.String(length=100), nullable=False),
        sa.Column('state', sa.String(length=2), nullable=False),
        sa.Column('complement', sa.String(length=100), nullable=True),
        sa.Column('poster_url', sa.String(length=500), nullable=True),
        sa.Column('banner_url', sa.String(length=500), nullable=True),
        sa.Column('custom_image_url', sa.String(length=500), nullable=True),
        sa.Column('maps_url', sa.String(length=500), nullable=False),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.CheckConstraint(
            'available_tickets >= 0', name='ck_events_available_tickets_positive'
        ),
        sa.CheckConstraint(
            'ticket_price >= 0.00', name='ck_events_ticket_price_positive'
        ),
        sa.CheckConstraint(
            'service_fee >= 0.00', name='ck_events_service_fee_positive'
        ),
        sa.ForeignKeyConstraint(['organizer_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_events_event_date'), 'events', ['event_date'])
    op.create_index(op.f('ix_events_city_slug'), 'events', ['city_slug'])

    op.create_table(
        'tickets',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('event_id', sa.Uuid(), nullable=False),
        sa.Column('user_id', sa.Uuid(), nullable=False),
        sa.Column(
            'status',
            sa.Enum('VALID', 'USED', 'CANCELLED', name='ticket_status'),
            nullable=False,
        ),
        sa.Column('qr_code_hash', sa.String(length=255), nullable=False),
        sa.Column(
            'purchased_at',
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column('validated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['event_id'], ['events.id']),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        'ix_tickets_user_status', 'tickets', ['user_id', 'status']
    )
    op.create_index(
        'ix_tickets_event_status', 'tickets', ['event_id', 'status']
    )

    op.create_table(
        'wallet_transactions',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('user_id', sa.Uuid(), nullable=False),
        sa.Column('event_id', sa.Uuid(), nullable=True),
        sa.Column('ticket_id', sa.Uuid(), nullable=True),
        sa.Column(
            'type',
            sa.Enum(
                'DEPOSIT',
                'TICKET_PURCHASE',
                'TICKET_REFUND',
                'EVENT_CREATION_FEE',
                'EVENT_PAYOUT',
                name='transaction_type',
            ),
            nullable=False,
        ),
        sa.Column('amount', sa.Numeric(10, 2), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=False),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(['event_id'], ['events.id']),
        sa.ForeignKeyConstraint(['ticket_id'], ['tickets.id']),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )

    op.create_table(
        'wallet_claim_tokens',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('token', sa.String(length=255), nullable=False),
        sa.Column('amount', sa.Numeric(10, 2), nullable=False),
        sa.Column(
            'type',
            sa.Enum(
                'DEPOSIT', 'TICKET_PURCHASE', 'EVENT_FEE',
                name='claim_token_type',
            ),
            nullable=False,
        ),
        sa.Column('target_id', sa.Uuid(), nullable=True),
        sa.Column('user_id', sa.Uuid(), nullable=True),
        sa.Column(
            'status',
            sa.Enum('PENDING', 'CLAIMED', 'EXPIRED', name='claim_token_status'),
            nullable=False,
        ),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('claimed_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(
        op.f('ix_wallet_claim_tokens_token'),
        'wallet_claim_tokens',
        ['token'],
        unique=True,
    )

    op.create_table(
        'event_payouts',
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.Column('event_id', sa.Uuid(), nullable=False),
        sa.Column('organizer_id', sa.Uuid(), nullable=False),
        sa.Column('gross_amount', sa.Numeric(10, 2), nullable=False),
        sa.Column('platform_fee_amount', sa.Numeric(10, 2), nullable=False),
        sa.Column('net_amount', sa.Numeric(10, 2), nullable=False),
        sa.Column(
            'status',
            sa.Enum(
                'PENDING', 'PROCESSING', 'PAID', 'FAILED', name='payout_status'
            ),
            nullable=False,
        ),
        sa.Column('scheduled_for', sa.DateTime(timezone=True), nullable=False),
        sa.Column('paid_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(['event_id'], ['events.id']),
        sa.ForeignKeyConstraint(['organizer_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('event_id'),
    )


def downgrade() -> None:
    op.drop_table('event_payouts')
    op.drop_index(
        op.f('ix_wallet_claim_tokens_token'), table_name='wallet_claim_tokens'
    )
    op.drop_table('wallet_claim_tokens')
    op.drop_table('wallet_transactions')
    op.drop_index('ix_tickets_event_status', table_name='tickets')
    op.drop_index('ix_tickets_user_status', table_name='tickets')
    op.drop_table('tickets')
    op.drop_index(op.f('ix_events_city_slug'), table_name='events')
    op.drop_index(op.f('ix_events_event_date'), table_name='events')
    op.drop_table('events')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')

    sa.Enum(name='payout_status').drop(op.get_bind())
    sa.Enum(name='claim_token_status').drop(op.get_bind())
    sa.Enum(name='claim_token_type').drop(op.get_bind())
    sa.Enum(name='transaction_type').drop(op.get_bind())
    sa.Enum(name='ticket_status').drop(op.get_bind())
    sa.Enum(name='event_status').drop(op.get_bind())
    sa.Enum(name='user_role').drop(op.get_bind())
