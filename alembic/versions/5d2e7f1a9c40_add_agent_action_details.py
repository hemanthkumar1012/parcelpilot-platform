"""add details to agent_actions

The escalation tool stores the escalation reason here. Before this column existed,
prepare_escalation failed with "'details' is an invalid keyword argument".

Revision ID: 5d2e7f1a9c40
Revises: 4c0cec259d3b
Create Date: 2026-11-22 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '5d2e7f1a9c40'
down_revision = '4c0cec259d3b'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('agent_actions', sa.Column('details', sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column('agent_actions', 'details')
