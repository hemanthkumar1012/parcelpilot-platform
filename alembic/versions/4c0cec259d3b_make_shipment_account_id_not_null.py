"""make shipment account_id not null

Revision ID: 4c0cec259d3b
Revises: 3b0bdb148c2a
Create Date: 2026-09-02 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '4c0cec259d3b'
down_revision = '3b0bdb148c2a'
branch_labels = None
depends_on = None

def upgrade() -> None:
    # batch mode: SQLite cannot ALTER a column in place, so Alembic copies the table.
    # On PostgreSQL this is a normal ALTER COLUMN.
    with op.batch_alter_table('shipments') as batch_op:
        batch_op.alter_column('account_id', existing_type=sa.INTEGER(), nullable=False)

def downgrade() -> None:
    with op.batch_alter_table('shipments') as batch_op:
        batch_op.alter_column('account_id', existing_type=sa.INTEGER(), nullable=True)
